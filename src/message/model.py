from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class ProviderCred:
    project_id: Optional[str] = None
    auth_token: Optional[str] = None


@dataclass
class Notification:
    title: Optional[str] = None
    body: Optional[str] = None
    image: Optional[str] = None


@dataclass
class AndroidNotification:
    title: Optional[str] = None
    body: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    image: Optional[str] = None
    channel_id: Optional[str] = None
    click_action: Optional[str] = None


@dataclass
class Android:
    ttl: Optional[str] = None
    notification: Optional[AndroidNotification] = None


@dataclass
class Message:
    notification: Optional[Notification] = None
    android: Optional[Android] = None


@dataclass
class VKPNSMessage:
    providers: Optional[Dict[str, ProviderCred]] = field(default_factory=dict)
    tokens: Optional[Dict[str, List[str]]] = field(default_factory=dict)
    message: Optional[Message] = None