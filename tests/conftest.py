import pytest as pytest


@pytest.fixture
def anyio_backend():
    """Tell anyio to use asyncio as backend, else it will try to use trio, which is not installed."""
    return 'asyncio'
