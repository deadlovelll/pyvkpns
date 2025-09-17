from typing import List
from dataclasses import asdict

from src.utils import remove_none, convert_empty_to_none
from src.message.model import (
    VKPNSMessage,
    ProviderCred,
    Message,
    Notification,
    Android,
    AndroidNotification,
)


class MessagePreparer:
    
    def prepare(
        self,
        project_id: str,
        auth_token: str,
        platform: str,
        tokens: List[str],
        title: str,
        body: str ,
        ttl: str = None,
        icon: str = None,
        image: str = None,
        channel_id: str = None,
        click_action: str = None,
        color: str = None,
    ) -> None:
        
        json = VKPNSMessage(
            providers={
                f'{platform}': ProviderCred(
                    project_id=project_id,
                    auth_token=auth_token,
                ),
            },
            tokens={
                f'{platform}': tokens,
            },
            message=Message(
                notification=Notification(
                    title=title,
                    body=body,
                ),
                android=Android(
                    ttl=ttl,
                    notification=AndroidNotification(
                        title=title,
                        body=body,
                        icon=icon,
                        color=color,
                        image=image,
                        channel_id=channel_id,
                        click_action=click_action,
                    ),
                ),
            ),
        )
        
        data = asdict(json)
        clear_data = convert_empty_to_none(data)
        return remove_none(clear_data)