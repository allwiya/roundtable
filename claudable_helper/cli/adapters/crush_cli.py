"""Crush CLI adapter for Roundtable AI MCP Server."""

import asyncio
from datetime import datetime
from pathlib import Path
from typing import Any, AsyncIterator, Dict, List, Optional

from claudable_helper.cli.base import BaseCLI
from claudable_helper.models.messages import Message, MessageType


class CrushCLI(BaseCLI):
    def __init__(self):
        super().__init__()
        self.cli_type = "crush"

    async def check_availability(self) -> Dict[str, Any]:
        try:
            proc = await asyncio.create_subprocess_shell("crush --help", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await proc.communicate()
            return {"available": proc.returncode == 0, "status": "✅ Crush CLI Available" if proc.returncode == 0 else f"❌ Crush CLI failed"}
        except Exception as e:
            return {"available": False, "status": f"❌ Crush CLI error: {str(e)}"}

    async def execute_with_streaming(self, instruction: str, project_path: str, session_id: Optional[str] = None, model: Optional[str] = None, images: Optional[List[Dict[str, Any]]] = None, is_initial_prompt: bool = False) -> AsyncIterator[Message]:
        project_path = str(Path(project_path).absolute())
        cmd = ["crush", instruction, "--project", project_path]
        try:
            proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, cwd=project_path)
            if proc.stdout:
                async for line in proc.stdout:
                    line_text = line.decode().strip()
                    if line_text:
                        yield Message(project_id=project_path, role="assistant", message_type=MessageType.TEXT, content=line_text, session_id=session_id or "default", created_at=datetime.utcnow())
            await proc.wait()
        except Exception as e:
            yield Message(project_id=project_path, role="assistant", message_type=MessageType.ERROR, content=f"Error: {str(e)}", session_id=session_id or "default", created_at=datetime.utcnow())
