import logging
import asyncio
from typing import Any, MutableMapping, Callable, Optional

import gi

gi.require_version("Gst", "1.0")
from gi.repository import Gst

from mixtape import hookimpl
from mixtape.exceptions import PlayerPipelineError

logger = logging.getLogger("mixtape.BoomBox")


@hookimpl
def setup(player) -> None:
    logger.debug("%s: setup completed.", player)


@hookimpl
def teardown(player) -> None:
    logger.debug("%s: teardown completed.", player)

