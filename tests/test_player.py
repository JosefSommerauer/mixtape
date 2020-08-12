# type: ignore
import pytest
import asyncio

import gi

gi.require_version("Gst", "1.0")
from gi.repository import Gst

from mixtape.player import Player
from mixtape.exceptions import PlayerSetStateError


def test_base_player_init_and_default_props(pipeline):
    player = Player(pipeline=pipeline)

    assert player.pipeline == pipeline
    assert player.state == Gst.State.NULL


@pytest.mark.parametrize(
    "method, state",
    [("ready", Gst.State.READY), ("play", Gst.State.PLAYING), ("pause", Gst.State.PAUSED)],
)
@pytest.mark.asyncio
async def test_player_async_methods(pipeline, mocker, method, state):
    player = Player(pipeline)
    player.setup()
    spy = mocker.spy(player.pipeline, "set_state")

    action = getattr(player, method)
    await asyncio.wait_for(action(), 1)
    spy.assert_called_with(state)
    player.teardown()


@pytest.mark.asyncio
async def test_async_player_exception(error_pipeline):
    """
    If we get a direct error from Gst.pipeline.set_state
    an exception should be returned inmediately
    """
    player = Player(error_pipeline)
    player.setup()

    with pytest.raises(PlayerSetStateError):
        await player.play()
    player.teardown()


@pytest.mark.asyncio
async def test_async_player_sequence(pipeline):
    """
    If we get a direct error from Gst.pipeline.set_state
    an exception should be returned inmediately
    """
    player = await Player.create(pipeline)

    sequence = ["ready", "play", "pause", "play", "stop"]
    for step in sequence:
        await getattr(player, step)()
        await asyncio.sleep(1)
    player.teardown()


@pytest.mark.asyncio
async def test_player_properties(Gst, pipeline):
    player = await Player.create(pipeline)
    # TODO: test type
    assert len(list(player.sinks)) == 1
    assert len(list(player.sinks)) == 1
    assert len(list(player.elements)) == 3
