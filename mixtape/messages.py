import mixtape




class Messages:
    """
    Gst.Bus message handler.
    Default handling sets the player asyncio events enabling
    the asyncio Player interface on default actions.
    """

    def __init__(self, player):
        
        self.bus: Gst.Bus = self.player.pipeline.get_bus()
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        self.pollfd: Any = None

 self.loop = asyncio.get_running_loop()
        self.pollfd = self.bus.get_pollfd()
        self.loop.add_reader(self.pollfd.fd, self.handle)


    def handle(self) -> None:
        """
        Asyncio reader callback, called when a message is available on
        the bus.
        """
        msg = self.bus.pop()
        if msg:
            handler = self.handlers.get(msg.type, self.on_unhandled_msg)
            handler(self.bus, msg)


    @property
    def handlers(self) -> MutableMapping[Gst.MessageType, Callable[[Gst.Bus, Gst.Message], None]]:
        """Returns default message handling mapping"""
        return {
            Gst.MessageType.ERROR: self.on_error,
            Gst.MessageType.EOS: self.on_eos,
            Gst.MessageType.STATE_CHANGED: self.on_state_changed,
        }

    def on_state_changed(self, bus: Gst.Bus, message: Gst.Message) -> None:
        """
        Handler for `state_changed` messages
        """
        old, new, _ = message.parse_state_changed()

        if message.src != self.player.pipeline:
            return
        logger.debug(
            "%s: state changed received from pipeline from %s to %s on %s",
            self.player,
            Gst.Element.state_get_name(old),
            Gst.Element.state_get_name(new),
            bus,
        )

        self.player.events.pick_state(new)

    def on_error(self, bus: Gst.Bus, message: Gst.Message) -> None:
        """
        Handler for `error` messages
        By default it will parse the error message,
        log to `error` and append to `self.errors`
        """
        err, debug = message.parse_error()
        self.player.events.error.set()
        logger.error(
            "Error received from element %s:%s on %s", message.src.get_name(), err.message, bus
        )
        if debug is not None:
            logger.error("Debugging information: %s", debug)
        # TODO: Cleanup on bus error message. self.player.teardown()
        raise PlayerPipelineError(err)

    def on_eos(self, bus: Gst.Bus, message: Gst.Message) -> None:
        """
        Handler for eos messages
        By default it sets the eos event
        """
        self.player.events.eos.set()
        logger.info("EOS message: %s received from pipeline on %s", message, bus)

    def on_unhandled_msg(self, bus: Gst.Bus, message: Gst.Message) -> None:
        """
        Handler for all other messages.
        By default will just log with `debug`
        """
        logger.debug("Unhandled msg: %s on %s", message.type, bus)



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

    @hookimpl
    def setup(self) -> None:
        self.messages = Messages()
       

    @hookimpl
    def teardown(self) -> None:
        if self.loop:
            self.loop.remove_reader(self.pollfd.fd)
        self.pollfd = None
        self.loop = None
    
    @mixtape.hookimpl
    def mixtape_addhooks(self):
        return MessageQueueSpec

    @mixtape.hookimpl
    def mixtape_register_action(self):
        return 




    # -- actions -- #

        