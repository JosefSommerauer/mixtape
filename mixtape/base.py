import logging
from typing import Any, Optional, Type, TypeVar, Tuple, List

import attr
import pluggy

import attr
import gi

gi.require_version("Gst", "1.0")
from gi.repository import Gst

from .exceptions import PlayerSetStateError


logger = logging.getLogger(__name__)

BasePlayerType = TypeVar("BasePlayerType", bound="BasePlayer")


@attr.s
class BasePlayer:
    """Player base player"""

    pipeline: Gst.Pipeline = attr.ib()
    plugins: Type[pluggy.PluginManager] = attr.ib(repr=False)
    
    def __del__(self) -> None:
        """
        Make sure that the gstreamer pipeline is always cleaned up
        """
        if self.state is not Gst.State.NULL:
            logger.warning("Player cleanup on destructor")
            self.teardown()

    @property
    def state(self) -> Gst.State:
        """Convenience property for the current pipeline Gst.State"""
        return self.pipeline.get_state(0)[1]

    def set_state(self, state: Gst.State) -> Tuple[Gst.StateChangeReturn, Gst.State, Gst.State]:
        """Set pipeline state"""
        ret = self.pipeline.set_state(state)
        if ret == Gst.StateChangeReturn.FAILURE:
            raise PlayerSetStateError
        return ret

    @property
    def hook(self) -> Any:
        """Convenience shortcut for pm hook"""
        return self.plugins.hook

    @property
    def sinks(self) -> List[Any]:
        """Returns all sink elements"""
        return list(self.pipeline.iterate_sinks())

    @property
    def sources(self) -> List[Any]:
        """Return all source elements"""
        return list(self.pipeline.iterate_sources())

    @property
    def elements(self) -> List[Any]:
        """Return all pipeline elements"""
        return list(self.pipeline.iterate_elements())

    def get_elements_by_gtype(self, gtype: Any) -> List[Any]:
        """Return all elements in pipeline that match gtype"""
        return [e for e in self.elements if e.get_factory().get_element_type() == gtype]
    def setup(self) -> None:
        """Player setup: meant to be used with hooks or subclassed"""

    def teardown(self) -> None:
        """Player teardown: by default sets the pipeline to Gst.State.NULL"""
        if self.state is not Gst.State.NULL:
            self.set_state(Gst.State.NULL)

    def _ready(self) -> Tuple[Gst.StateChangeReturn, Gst.State, Gst.State]:
        """Set pipeline to state to Gst.State.READY"""
        return self.set_state(Gst.State.READY)

    def _play(self) -> Tuple[Gst.StateChangeReturn, Gst.State, Gst.State]:
        """Set pipeline to state to Gst.State.PLAY"""
        return self.set_state(Gst.State.PLAYING)

    def _pause(self) -> Tuple[Gst.StateChangeReturn, Gst.State, Gst.State]:
        """Set pipeline to state to Gst.State.PAUSED"""
        return self.set_state(Gst.State.PAUSED)

    def _stop(self) -> Tuple[Gst.StateChangeReturn, Gst.State, Gst.State]:
        """Set pipeline to state to Gst.State.NULL"""
        return self.set_state(Gst.State.NULL)
