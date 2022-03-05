import pytest

from client.client import Client


@pytest.mark.asyncio
class TestClient:
    def setup(self):
        self.client = Client()

    async def test_get_users(self):
        async with self.client as client:
            resp = await client.get_users()
            assert resp == ""
