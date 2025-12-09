"""Rovo Dev CLI adapter for Roundtable AI MCP Server."""

import asyncio
from datetime import datetime
from pathlib import Path
from typing import Any, AsyncIterator, Dict, List, Optional

from claudable_helper.cli.base import BaseCLI
from claudable_helper.models.messages import Message, MessageType


class RovoCLI(BaseCLI):
    def __init__(self):
        super().__init__(cli_type="rovo")
        self.session_mapping: Dict[str, str] = {}

    async def check_availability(self) -> Dict[str, Any]:
        try:
            proc = await asyncio.create_subprocess_shell("acli rovodev --help", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await proc.communicate()
            return {"available": proc.returncode == 0, "status": "✅ Rovo Dev CLI Available" if proc.returncode == 0 else f"❌ Rovo Dev CLI failed"}
        except Exception as e:
            return {"available": False, "status": f"❌ Rovo Dev CLI error: {str(e)}"}

    async def execute_with_streaming(self, instruction: str, project_path: str, session_id: Optional[str] = None, model: Optional[str] = None, images: Optional[List[Dict[str, Any]]] = None, is_initial_prompt: bool = False) -> AsyncIterator[Message]:
        project_path = str(Path(project_path).absolute())
        cmd = ["acli", "rovodev", "run", instruction]
        try:
            proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, cwd=project_path)
            if proc.stdout:
                async for line in proc.stdout:
                    line_text = line.decode().strip()
                    if line_text:
                        yield Message(project_id=project_path, role="assistant", message_type=MessageType.ASSISTANT, content=line_text, session_id=session_id or "default", created_at=datetime.utcnow())
            await proc.wait()
        except Exception as e:
            yield Message(project_id=project_path, role="assistant", message_type=MessageType.ERROR, content=f"Error: {str(e)}", session_id=session_id or "default", created_at=datetime.utcnow())

    async def get_session_id(self, project_id: str) -> Optional[str]:
        """Get current session ID for project"""
        return self.session_mapping.get(project_id)

    async def set_session_id(self, project_id: str, session_id: str) -> None:
        """Set session ID for project in memory"""
        self.session_mapping[project_id] = session_id
