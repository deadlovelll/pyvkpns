import pytest
from aioresponses import aioresponses
from pyvkpns.http_client import HttpClient
from pyvkpns.credentials import VKPNS_LINK

import pytest_asyncio

@pytest_asyncio.fixture
async def client():
    c = HttpClient()
    yield c
    await c.close()


@pytest.mark.asyncio
class TestHttpClient:

    async def test_singleton_behavior(self, client):
        client2 = HttpClient()
        assert client is client2, "HttpClient should be a singleton"

    async def test_get_session_creates_session(self, client):
        session = await client._get_session()
        assert session is not None
        assert not session.closed

    async def test_get_session_reuses_session(self, client):
        session1 = await client._get_session()
        session2 = await client._get_session()
        assert session1 is session2

    async def test_send_returns_json(self, client):
        payload = {"message": "hello"}
        expected_response = {"status": "ok"}

        with aioresponses() as mocked:
            mocked.post(VKPNS_LINK, payload=expected_response)
            response = await client.send(payload)
            assert response == expected_response

    async def test_close_session(self, client):
        session = await client._get_session()
        await client.close()
        assert session.closed