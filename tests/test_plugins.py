import pytest
import asyncio

@pytest.mark.asyncio
async def test_mixtape_create(Gst):
    import mixtape

    pm = mixtape.init_plugin_manager()
    # p = mixtape.create("plugin", hello="hello", something=3)
    import pdb; pdb.set_trace()