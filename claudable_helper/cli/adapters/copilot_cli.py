"""GitHub Copilot CLI adapter for Roundtable AI MCP Server."""

import asyncio
from datetime import datetime
from pathlib import Path
from typing import Any, AsyncIterator, Dict, List, Optional

from claudable_helper.cli.base import BaseCLI
from claudable_helper.core.terminal_ui import ui
from claudable_helper.models.messages import Message, MessageType


class CopilotCLI(BaseCLI):
    """Adapter for GitHub Copilot CLI."""

    def __init__(self):
        super().__init__()
        self.cli_type = "copilot"

    async def check_availability(self) -> Dict[str, Any]:
        """Check if GitHub Copilot CLI is available."""
        try:
            proc = await asyncio.create_subprocess_shell(
                "gh copilot --help",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await proc.communicate()

            if proc.returncode == 0:
                return {
                    "available": True,
                    "status": "✅ GitHub Copilot CLI Available",
                    "version": "latest",
                }
            else:
                return {
                    "available": False,
                    "status": f"❌ GitHub Copilot CLI failed: {stderr.decode()}",
                }
        except Exception as e:
            return {
                "available": False,
                "status": f"❌ GitHub Copilot CLI error: {str(e)}",
            }

    async def execute_with_streaming(
        self,
        instruction: str,
        project_path: str,
        session_id: Optional[str] = None,
        model: Optional[str] = None,
        images: Optional[List[Dict[str, Any]]] = None,
        is_initial_prompt: bool = False,
    ) -> AsyncIterator[Message]:
        """Execute GitHub Copilot CLI with streaming output."""
        
        project_path = str(Path(project_path).absolute())

        # Build command - gh copilot suggest
        cmd = [
            "gh",
            "copilot",
            "suggest",
            instruction,
        ]

        ui.info(f"Executing GitHub Copilot CLI: {' '.join(cmd)}", "CopilotCLI")

        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=project_path,
            )

            # Stream stdout
            if proc.stdout:
                async for line in proc.stdout:
                    line_text = line.decode().strip()
                    if line_text:
                        yield Message(
                            project_id=project_path,
                            role="assistant",
                            message_type=MessageType.TEXT,
                            content=line_text,
                            session_id=session_id or "default",
                            created_at=datetime.utcnow(),
                        )

            await proc.wait()

            if proc.returncode != 0 and proc.stderr:
                stderr = await proc.stderr.read()
                error_msg = stderr.decode().strip()
                yield Message(
                    project_id=project_path,
                    role="assistant",
                    message_type=MessageType.ERROR,
                    content=f"GitHub Copilot CLI error: {error_msg}",
                    session_id=session_id or "default",
                    created_at=datetime.utcnow(),
                )

        except Exception as e:
            ui.error(f"GitHub Copilot CLI execution failed: {str(e)}", "CopilotCLI")
            yield Message(
                project_id=project_path,
                role="assistant",
                message_type=MessageType.ERROR,
                content=f"Execution error: {str(e)}",
                session_id=session_id or "default",
                created_at=datetime.utcnow(),
            )
