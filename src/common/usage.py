"""
Usage system.

(C) 2022-2026 - B1ue-Dev
"""

import logging
from datetime import datetime

import interactions

from src.common import error_handler
from src.common.models import usage as usage_db


class Usage(interactions.Extension):
    """Usage logging."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.listen()
    async def on_command_completion(
        self,
        event: interactions.events.CommandCompletion,
    ) -> None:
        """For CommandError callback."""

        cmd_name = event.ctx.invoke_target

        if error_handler.debug_system:
            return

        if isinstance(
            event.ctx, interactions.ext.prefixed_commands.PrefixedContext
        ):
            return

        try:
            log = usage_db(
                command_name=cmd_name,
                timestamp=datetime.now(),
                user_id=int(event.ctx.user.id),
            )
            await log.insert()
        except Exception as e:
            logging.error(f"Failed to log command completion to MongoDB: {e}")
