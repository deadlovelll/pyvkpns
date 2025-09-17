from typing import Dict, Union
import aiohttp

from src.credentials import VKPNS_LINK, HEADERS


class HttpClient:
    
    _instance = None
    _session: aiohttp.ClientSession | None = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def send(
        self,
        payload: Dict[str, Union[str, Dict]],
    ) -> Dict[str, Union[str, Dict]]:
        
        session = await self._get_session()
        async with session.post(
            url=VKPNS_LINK,
            headers=HEADERS,
            json=payload,
            timeout=5,
        ) as response:
            return await response.json()

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()