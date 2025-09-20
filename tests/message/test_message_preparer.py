import pytest

from tests.utils import assert_no_none
from src.pyvkpns.message.preparer import MessagePreparer

class TestMessagePreparer:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.preparer = MessagePreparer()

    def test_prepare_basic(self):
        result = self.preparer.prepare(
            project_id="proj_123",
            auth_token="token_abc",
            platform="fcm",
            tokens=["token1", "token2"],
            title="Hello",
            body="World",
            ttl="3600s",
            icon="icon.png",
            image="image.png",
            channel_id="channel_1",
            click_action="OPEN_APP",
            color="#FF0000"
        )

        assert isinstance(result, dict)
        assert "providers" in result
        assert "fcm" in result["providers"]
        assert result["providers"]["fcm"]["project_id"] == "proj_123"
        assert result["providers"]["fcm"]["auth_token"] == "token_abc"
        assert "tokens" in result
        assert result["tokens"]["fcm"] == ["token1", "token2"]
        msg = result["message"]
        assert msg["notification"]["title"] == "Hello"
        assert msg["notification"]["body"] == "World"
        android = msg["android"]
        assert android["ttl"] == "3600s"
        notif = android["notification"]
        assert notif["title"] == "Hello"
        assert notif["body"] == "World"
        assert notif["icon"] == "icon.png"
        assert notif["color"] == "#FF0000"
        assert notif["image"] == "image.png"
        assert notif["channel_id"] == "channel_1"
        assert notif["click_action"] == "OPEN_APP"

    @pytest.mark.parametrize("platform", ["fcm", "huawei", "apns"])
    def test_prepare_platforms(self, platform):
        result = self.preparer.prepare(
            project_id="proj",
            auth_token="tok",
            platform=platform,
            tokens=["t1"],
            title="T",
            body="B",
            ttl="100s",
            icon="i.png",
            image="im.png",
            channel_id="c",
            click_action="click",
            color="#000"
        )
        assert platform in result["providers"]
        assert platform in result["tokens"]

    def test_prepare_empty_optional_fields(self):
        result = self.preparer.prepare(
            project_id="",
            auth_token="",
            platform="fcm",
            tokens=[],
            title="",
            body="",
            ttl="",
            icon="",
            image="",
            channel_id="",
            click_action="",
            color=""
        )
        msg = result["message"]
        assert msg["notification"] is not None
        assert msg["android"]["notification"] is not None
        assert msg["notification"]["title"] == ""
        assert msg["notification"]["body"] == ""
        android_notif = msg["android"]["notification"]
        assert android_notif["title"] == ""
        assert android_notif["body"] == ""

    def test_prepare_multiple_tokens(self):
        tokens = ["tok1", "tok2", "tok3"]
        result = self.preparer.prepare(
            project_id="proj",
            auth_token="tok",
            platform="fcm",
            tokens=tokens,
            title="Hi",
            body="Body",
            ttl="10s",
            icon="icon",
            image="img",
            channel_id="chan",
            click_action="act",
            color="#123"
        )
        assert result["tokens"]["fcm"] == tokens
        
    def test_no_none_basic(self):
        result = self.preparer.prepare(
            project_id="proj_123",
            auth_token="token_abc",
            platform="fcm",
            tokens=["token1", "token2"],
            title="Hello",
            body="World",
            ttl="3600s",
            icon="icon.png",
            image="image.png",
            channel_id="channel_1",
            click_action="OPEN_APP",
            color="#FF0000"
        )
        assert_no_none(result)

    def test_prepare_empty_optional_fields(self):
        result = self.preparer.prepare(
            project_id="",
            auth_token="",
            platform="fcm",
            tokens=[],
            title="",
            body="",
            ttl="",
            icon="",
            image="",
            channel_id="",
            click_action="",
            color=""
        )
        msg = result["message"]

        assert "title" not in msg["notification"]
        assert "body" not in msg["notification"]

        android_notif = msg["android"]["notification"]
        assert "title" not in android_notif
        assert "body" not in android_notif