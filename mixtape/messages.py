import mixtape

class MessageQueueSpec:
    
    @mixtape.hookspecs.hookspec
    def messages_on_eos(self):
        pass

    @mixtape.hookspecs.hookspec
    def messages_on_error(self):
        pass

    @mixtape.hookspecs.hookspec
    def messages_on_qos(self):
        pass


class MessageQueuePlugin:
    
    # @mixtape.hookimpl
    # def mixtape_addoption(self):
    #     return "silent"

    @mixtape.hookimpl
    def mixtape_addhooks(self):
        return MessageQueueSpec

    @mixtape.hookimpl
    def mixtape_register_action(self):
        return 


    # -- actions -- #

        