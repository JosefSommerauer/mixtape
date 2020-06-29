from pluggy import HookspecMarker


hookspec = HookspecMarker("mixtape")



# plugins and config


@hookspec
def mixtape_addhooks():
    pass

@hookspec
def mixtape_plugin_registered():
    pass

@hookspec
def mixtape_plugin_autoload():
    pass

@hookspec
def mixtape_addoption():
    pass

@hookspec
def mixtape_configure():
    pass

# pipeline creation and signals

@hookspec
def create_pipeline():
    pass

@hookspec
def mixtape_on_deep_element_added():
    pass

@hookspec
def mixtape_on_deep_element_removed():
    pass

@hookspec
def mixtape_on_element_added():
    pass


# player init and teardown

@hookspec
def mixtape_init(conf, pipeline):
    pass

@hookspec
def mixtape_teardown(conf, pipeline):
    pass


# pipeline control and event hooks

@hookspec
def mixtape_pre_state_change():
    pass

@hookspec
def mixtape_on_state_change():
    pass

@hookspec
def mixtape_pre_eos():
    pass

@hookspec
def mixtape_on_eos():
    pass


# player actions and properties


@hookspec
def mixtape_register_action():
    pass

@hookspec
def mixtape_register_property():
    pass