import unittest
from unittest.mock import AsyncMock, patch
from pyvkpns.client import VKPNSClient
from pyvkpns.exceptions import (
    ValidationErrorException, 
    ProviderErrorException,
)


class TestVKPNSClient(unittest.IsolatedAsyncioTestCase):
    
    def setUp(self):
        self.project_id = "test_project"
        self.service_token = "test_token"
        self.platform = "fcm"
        
        self.patcher_http = patch(
            "src.pyvkpns.client.HttpClient", 
            autospec=True,
        )
        self.patcher_preparer = patch(
            "src.pyvkpns.client.MessagePreparer", 
            autospec=True,
        )
        self.patcher_validator = patch(
            "src.pyvkpns.client.ResponseValidator", 
            autospec=True,
        )
        
        self.mock_http_cls = self.patcher_http.start()
        self.mock_preparer_cls = self.patcher_preparer.start()
        self.mock_validator_cls = self.patcher_validator.start()
        
        self.addCleanup(self.patcher_http.stop)
        self.addCleanup(self.patcher_preparer.stop)
        self.addCleanup(self.patcher_validator.stop)
        
        self.client = VKPNSClient(
            project_id=self.project_id,
            service_token=self.service_token,
            platform=self.platform
        )
        
        self.mock_http_instance = self.mock_http_cls.return_value
        self.mock_http_instance.send = AsyncMock()
        
        self.mock_preparer_instance = self.mock_preparer_cls.return_value
        self.mock_preparer_instance.prepare.return_value = {
            "data": "prepared"
        }
        
        self.mock_validator_instance = self.mock_validator_cls.return_value
        self.mock_validator_instance.validate.return_value = None

    async def test_send_notification_calls_all_dependencies(self):
        tokens = ["token1", "token2"]
        title = "Test Title"
        body = "Test Body"
        
        await self.client.send_notification(
            tokens=tokens, 
            title=title, 
            body=body,
        )
        
        self.mock_preparer_instance.prepare.assert_called_once_with(
            self.project_id,
            self.service_token,
            platform=self.platform,
            title=title,
            body=body,
            ttl=None,
            icon=None,
            image=None,
            channel_id=None,
            click_action=None,
            tokens=tokens,
            color=None,
        )
        
        self.mock_http_instance.send.assert_awaited_once_with(
            {
                "data": "prepared"
            }
        )
        
        self.mock_validator_instance.validate.assert_called_once_with(
            self.mock_http_instance.send.return_value
        )

    async def test_send_notification_raises_validation_error(self):
        self.mock_validator_instance.validate.side_effect = (
            ValidationErrorException("Invalid")
        )
        
        with self.assertRaises(ValidationErrorException):
            await self.client.send_notification(
                tokens=["t"], 
                title="t", 
                body="b",
            )

    async def test_send_notification_raises_provider_error(self):
        self.mock_validator_instance.validate.side_effect = (
            ProviderErrorException("Provider error")
        )
        
        with self.assertRaises(ProviderErrorException):
            await self.client.send_notification(
                tokens=["t"], 
                title="t", 
                body="b",
            )