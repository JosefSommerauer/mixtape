import sys
from typing import (Any, Callable, List, Mapping, MutableMapping, Optional,
                    Tuple, Type, TypeVar)

# from mixtape.core import BoomBox
import pluggy

# from .core import BoomBox
from .player import Player
from . import hookspecs


hookimpl = pluggy.HookimplMarker("mixtape")

def load_plugin_manager(plugins=None):
    """Init mixtape plugin manager"""

    if plugins is None:
        plugins = []
    pm = pluggy.PluginManager(__name__)
    pm.add_hookspecs(hookspecs)
    pm.load_setuptools_entrypoints(group=__name__) 
    return pm


# def create(pipeline=None, plugins=None, **options):
#     # type: (Optional[Gst.Pipeline], Optional[List[object]], MutableMapping[str, Any]) -> BoomBox
#     """Player factory"""
#     return BoomBox(pipeline, init_plugin_manager(plugins), options)


# def from_description(description, plugins=None, **options):
#     # type: (str, Optional[List[object]], MutableMapping[str, Any]) -> BoomBox
#     """Player factory from description"""
#     pipeline = Gst.parse_launch(description)
#     return BoomBox(pipeline, init_plugin_manager(plugins), options)
