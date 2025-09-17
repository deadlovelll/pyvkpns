from typing import List

from src.http_client import HttpClient
from src.message.preparer import MessagePreparer


class VKPNSClient:
    
    def __init__(
        self,
        project_id: str,
        service_token: str,
        platform: str,
    ) -> None:
        
        self._project_id = project_id
        self._service_token = service_token
        self._platform = platform
        self._client = HttpClient()
        self._message_preparer = MessagePreparer()
    
    async def send_notification(
        self,
        tokens: List[str],
        title: str,
        body: str,
        ttl: str = None,
        icon: str = None,
        image: str = None,
        channel_id: str = None,
        click_action: str = None,
        color: str = None,
    ) -> None:
        
        data = self._message_preparer.prepare(
            self._project_id,
            self._service_token,
            platform=self._platform,
            title=title,
            body=body,
            ttl=ttl,
            icon=icon,
            image=image,
            channel_id=channel_id,
            click_action=click_action,
            click_action=click_action,
            tokens=tokens,
            color=color,
        )
        response = await self._client.send(data)