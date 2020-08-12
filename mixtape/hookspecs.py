from pluggy import HookspecMarker


hookspec = HookspecMarker("mixtape")



# plugins and config


@hookspec
def mixtape_addhooks():
    pass

# @hookspec
# def mixtape_plugin_registered(player, pipeline, options):
#     pass

# @hookspec
# def mixtape_plugin_autoload(player, pipeline, options):
#     pass

# @hookspec
# def mixtape_addoption(player):
#     pass

# @hookspec
# def mixtape_configure():
#     pass

# pipeline creation and signals

# @hookspec
# def mixtape_create_pipeline(player):
#     pass

# @hookspec
# def mixtape_on_element_added(player, element):
#     pass

# @hookspec
# def mixtape_on_deep_element_added(player, element):
#     pass

# @hookspec
# def mixtape_on_deep_element_removed(player, element):
#     pass


# player init and teardown

@hookspec
def mixtape_init(pipeline, options, commands, properties):
    pass

@hookspec
def mixtape_teardown(pipeline, options, commands, properties):
    pass


# pipeline control and event hooks

@hookspec
def mixtape_before_state_changed(state):
    pass

@hookspec
def mixtape_on_state_changed(state):
    pass

@hookspec
def mixtape_on_eos():
    pass


# player actions and properties


@hookspec
def mixtape_register_method():
    pass

@hookspec
def mixtape_register_property():
    pass