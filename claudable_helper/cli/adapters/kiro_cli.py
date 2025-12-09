"""Kiro CLI adapter for Roundtable AI MCP Server."""

import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, AsyncIterator, Dict, List, Optional

from claudable_helper.cli.base import BaseCLI
from claudable_helper.core.terminal_ui import ui
from claudable_helper.models.messages import Message, MessageType


class KiroCLI(BaseCLI):
    """Adapter for Kiro CLI."""

    def __init__(self):
        super().__init__(cli_type="kiro")

    async def check_availability(self) -> Dict[str, Any]:
        """Check if Kiro CLI is available."""
        try:
            proc = await asyncio.create_subprocess_shell(
                "kiro-cli --help",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await proc.communicate()

            if proc.returncode == 0:
                return {
                    "available": True,
                    "status": "✅ Kiro CLI Available",
                    "version": "latest",
                }
            else:
                return {
                    "available": False,
                    "status": f"❌ Kiro CLI failed: {stderr.decode()}",
                }
        except Exception as e:
            return {
                "available": False,
                "status": f"❌ Kiro CLI error: {str(e)}",
            }

    def _get_cli_model_name(self, model: Optional[str]) -> str:
        """Map generic model name to Kiro CLI model."""
        if not model:
            return "claude-sonnet-4"
        
        model_map = {
            "claude-3.5-sonnet": "claude-sonnet-4",
            "claude-opus": "claude-opus-4",
            "gpt-4": "gpt-4",
            "gpt-5": "gpt-5",
            "sonnet-4": "claude-sonnet-4",
        }
        return model_map.get(model, model)

    async def execute_with_streaming(
        self,
        instruction: str,
        project_path: str,
        session_id: Optional[str] = None,
        model: Optional[str] = None,
        images: Optional[List[Dict[str, Any]]] = None,
        is_initial_prompt: bool = False,
    ) -> AsyncIterator[Message]:
        """Execute Kiro CLI with streaming output."""
        
        cli_model = self._get_cli_model_name(model)
        project_path = str(Path(project_path).absolute())

        # Build command - Kiro uses current directory, no --project-path flag
        cmd = [
            "kiro-cli",
            "chat",
            "--no-interactive",
            "--trust-all-tools",
            instruction,
        ]

        if cli_model:
            cmd.extend(["--model", cli_model])

        ui.info(f"Executing Kiro CLI: {' '.join(cmd)}", "KiroCLI")

        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=project_path,  # Set working directory here
            )

            # Stream stdout
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
                error_msg = stderr.decode().strip()
                yield Message(
                    project_id=project_path,
                    role="assistant",
                    message_type=MessageType.ERROR,
                    content=f"Kiro CLI error: {error_msg}",
                    session_id=session_id or "default",
                    created_at=datetime.utcnow(),
                )

        except Exception as e:
            ui.error(f"Kiro CLI execution failed: {str(e)}", "KiroCLI")
            yield Message(
                project_id=project_path,
                role="assistant",
                message_type=MessageType.ERROR,
                content=f"Execution error: {str(e)}",
                session_id=session_id or "default",
                created_at=datetime.utcnow(),
            )

    async def get_session_id(self, project_id: str) -> Optional[str]:
        """Get session ID for project (Kiro doesn't use sessions)."""
        return None

    async def set_session_id(self, project_id: str, session_id: str) -> None:
        """Set session ID for project (Kiro doesn't use sessions)."""
        pass
