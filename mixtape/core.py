from typing import Any, Optional, Type, TypeVar, Tuple, List, Mapping, MutableMapping, Callable


import asyncio
import attr
import logging
import pluggy
import attr

from . import hookspecs

@attr.s
class BoomBox:
    "Boom boom"
    player: Any = attr.ib()
    pluggy: Type[pluggy.PluginManager] = attr.ib(repr=False)
    meta: MutableMapping[str, Any] = attr.ib(default=dict())

    @property
    def hook(self) -> Any:
        """Convenience shortcut for pm hook"""
        return self.pluggy.hook

    def add_property(self, prop: Any) -> None:
        """Add a property to the meta context"""
        pass

    def add_method(self, method: Callable[..., Any]) -> None:
        """Add a method to the meta context"""
        pass
