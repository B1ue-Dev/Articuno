"""
Custom Task implementation.

2026 - B1ue-Dev
"""

import asyncio
import logging
from collections.abc import Awaitable, Callable


periodic_tasks: set[asyncio.Task[None]] = set()


async def run_periodically(
    name: str,
    callback: Callable[[], Awaitable[None]],
    interval_seconds: int,
) -> None:

    while True:
        await asyncio.sleep(interval_seconds)
        try:
            await callback()
        except asyncio.CancelledError:
            raise
        except Exception:
            logging.exception("Periodic task '%s' failed", name)


def start_task(
    name: str,
    callback: Callable[[], Awaitable[None]],
    interval_seconds: int,
) -> None:

    task = asyncio.create_task(
        run_periodically(name, callback, interval_seconds),
        name=f"periodic:{name}",
    )
    periodic_tasks.add(task)
    task.add_done_callback(periodic_tasks.discard)


async def shutdown_tasks() -> None:

    tasks = tuple(periodic_tasks)
    for task in tasks:
        task.cancel()
    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)
