import logging
import asyncio
from typing import Any, MutableMapping, Callable, Optional

import gi

gi.require_version("Gst", "1.0")
from gi.repository import Gst

from mixtape.spec import hookimpl
from mixtape.exceptions import PlayerPipelineError

logger = logging.getLogger(__name__)


class MixtapePlugin:
    """
    Mixtape plugin base clase
    """

    def __init__(self, player: Any):
        self.player = player

    @hookimpl
    def setup(self) -> None:
        pass

    @hookimpl
    def teardown(self) -> None:
        pass

    # -- default actions -- #

    @hookimpl
    def on_ready(self) -> None:
        pass

    @hookimpl
    def on_play(self) -> None:
        pass

    @hookimpl
    def on_pause(self) -> None:
        pass

    @hookimpl
    def on_stop(self) -> None:
        pass


class Logger(MixtapePlugin):
    """
    Mixtape logging plugin.
    Purpose is mostly to dogfood the plugin spec
    """

    def __init__(self, player: Any):
        super().__init__(player)
        self.logger: logging.Logger = logging.getLogger(f"{self.player.__module__}")

    @hookimpl
    def setup(self) -> None:
        self.logger.debug("%s: setup completed.", self.player)

    @hookimpl
    def teardown(self) -> None:
        self.logger.debug("%s: teardown completed.", self.player)

    # -- default actions -- #

    @hookimpl
    def on_ready(self) -> None:
        self.logger.debug("%s: ready.", self.player)

    @hookimpl
    def on_play(self) -> None:
        self.logger.debug("%s: playing.", self.player)

    @hookimpl
    def on_pause(self) -> None:
        self.logger.debug("%s: paused.", self.player)

    @hookimpl
    def on_stop(self) -> None:
        self.logger.debug("%s: stopped.", self.player)

