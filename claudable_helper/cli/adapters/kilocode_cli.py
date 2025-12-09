"""Kilocode CLI adapter for Roundtable AI MCP Server."""

import asyncio
from datetime import datetime
from pathlib import Path
from typing import Any, AsyncIterator, Dict, List, Optional

from claudable_helper.cli.base import BaseCLI
from claudable_helper.core.terminal_ui import ui
from claudable_helper.models.messages import Message, MessageType


class KilocodeCLI(BaseCLI):
    """Adapter for Kilocode CLI."""

    def __init__(self):
        super().__init__(cli_type="kilocode")
        self.session_mapping: Dict[str, str] = {}

    async def check_availability(self) -> Dict[str, Any]:
        """Check if Kilocode CLI is available."""
        try:
            proc = await asyncio.create_subprocess_shell(
                "kilocode --help",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await proc.communicate()

            if proc.returncode == 0:
                return {"available": True, "status": "✅ Kilocode CLI Available"}
            else:
                return {"available": False, "status": f"❌ Kilocode CLI failed: {stderr.decode()}"}
        except Exception as e:
            return {"available": False, "status": f"❌ Kilocode CLI error: {str(e)}"}

    async def execute_with_streaming(
        self,
        instruction: str,
        project_path: str,
        session_id: Optional[str] = None,
        model: Optional[str] = None,
        images: Optional[List[Dict[str, Any]]] = None,
        is_initial_prompt: bool = False,
    ) -> AsyncIterator[Message]:
        """Execute Kilocode CLI with streaming output."""
        project_path = str(Path(project_path).absolute())
        cmd = ["kilocode", instruction, "--path", project_path]

        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=project_path,
            )

            if proc.stdout:
                async for line in proc.stdout:
                    line_text = line.decode().strip()
                    if line_text:
                        yield Message(
                            project_id=project_path,
                            role="assistant",
                            message_type=MessageType.ASSISTANT,
                            content=line_text,
                            session_id=session_id or "default",
                            created_at=datetime.utcnow(),
                        )

            await proc.wait()

            if proc.returncode != 0 and proc.stderr:
                stderr = await proc.stderr.read()
                yield Message(
                    project_id=project_path,
                    role="assistant",
                    message_type=MessageType.ERROR,
                    content=f"Kilocode CLI error: {stderr.decode().strip()}",
                    session_id=session_id or "default",
                    created_at=datetime.utcnow(),
                )

        except Exception as e:
            yield Message(
                project_id=project_path,
                role="assistant",
                message_type=MessageType.ERROR,
                content=f"Execution error: {str(e)}",
                session_id=session_id or "default",
                created_at=datetime.utcnow(),
            )

    async def get_session_id(self, project_id: str) -> Optional[str]:
        """Get current session ID for project"""
        return self.session_mapping.get(project_id)

    async def set_session_id(self, project_id: str, session_id: str) -> None:
        """Set session ID for project in memory"""
        self.session_mapping[project_id] = session_id
