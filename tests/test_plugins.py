import pytest
import asyncio

@pytest.mark.asyncio
async def test_mixtape_init_plugin_manager(Gst):
    import mixtape
    pm = mixtape.init_plugin_manager()