# from mixtape.players import Player
import pluggy

from . import hookspecs
hookimpl = pluggy.HookimplMarker("mixtape")

"""
Usage as a library vs usage as 


import mixtape

mixtape.create(pipeline, options, plugins)
mixtape.from_description("pipeline description", options, plugins)
"""
__all__ = ["Player"]

DEFAULT_PLUGINS = ["messages"]

class Host:

    def __init__(self, hook):
        self.hook = hook
    


def init_plugin_manager(plugins=None):
    if plugins is None:
        plugins = []
    
    pm = pluggy.PluginManager("mixtape")
    pm.add_hookspecs(hookspecs)
    for p in DEFAULT_PLUGINS + plugins:
        pm.load_setuptools_entrypoints("mixtape", p)
    # class based entry points not instatiated.
    for p in pm.get_plugins():
        try:
            isinstance(p, object)
        except TypeError:
            pass
        else:
            pm.unregister(p)
            pm.register(p())
    return pm


def create(pipeline, plugins=None, **options):
    return init_plugin_manager()


def from_description(desc, plugins, **options):
    return options