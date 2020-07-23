

import gi

gi.require_version("Gst", "1.0")
from gi.repository import Gst

from .base import BasePlayer
from .events import PlayerEvents
from .plugins import MixtapePlugin, Logger, MessageHandler
from .spec import PlayerSpec
from .exceptions import PlayerSetStateError

import mixtape
# PlayerT = TypeVar("PlayerT", bound="Player")
# MixtapePluginT = Type[MixtapePlugin]


@attr.s
class AsyncIO:
    """
    An asyncio compatible player.
    Interfaces with the `Gst.Bus` with an asyncio file descriptor,
    which is used to set `asyncio.Event` when received for the bus,
    allowing for asyncio compatible methods.
    """

    DEFAULT_METHODS = ['ready', 'play', 'pause', 'stop', 'send_eos']
    DEFAULT_PROPERTIES = ['state', 'sinks', 'sources', 'elements']

    pipeline: Gst.Pipeline = attr.ib()
   
    events: PlayerEvents = attr.ib(init=False, default=attr.Factory(PlayerEvents))

    # def __del__(self) -> None:
    #     """
    #     Make sure that the gstreamer pipeline is always cleaned up
    #     """
    #     if self.state is not Gst.State.NULL:
    #         self.teardown()

   

    # -- pipeline control -- #

    async def ready(self) -> Tuple[Gst.StateChangeReturn, Gst.State, Gst.State]:
        """Async override of base.ready"""
        ret = self.set_state(Gst.State.READY)
        await self.events.wait_for_state(Gst.State.READY)
        self.hook.on_ready()
        return ret

    async def play(self) -> Tuple[Gst.StateChangeReturn, Gst.State, Gst.State]:
        """Async override of base.play"""
        ret = self.set_state(Gst.State.PLAYING)
        await self.events.wait_for_state(Gst.State.PLAYING)
        self.hook.on_play()
        return ret

    async def pause(self) -> Tuple[Gst.StateChangeReturn, Gst.State, Gst.State]:
        """Async override of base.pause"""
        ret = self.set_state(Gst.State.PAUSE)
        await self.events.wait_for_state(Gst.State.PAUSED)
        self.hook.on_pause()
        return ret

    async def stop(self) -> Tuple[Gst.StateChangeReturn, Gst.State, Gst.State]:
        """Async override of base.stop"""
        ret = self.set_state(Gst.State.NULL)
        self.hook.on_stop()
        return ret

    async def send_eos(self) -> bool:
        """Send eos to pipeline and await event"""
        ret = self.pipeline.send_event(Gst.Event.new_eos())
        await self.events.eos.wait()
        self.hook.on_eos()
        return ret

    # -- setup and teaddown -- #

    def setup(self) -> None:
        """Setup needs a running asyncio loop"""
        self.hook.setup()
        self.events.setup.set()

    def teardown(self) -> None:
        """Cleanup player references to loop and gst resources"""
        self.hook.teardown()
        if self.state is not Gst.State.NULL:
            self.set_state(Gst.State.NULL)
        self.events.teardown.set()

 