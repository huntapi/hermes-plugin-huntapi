"""Unit tests for the HuntAPI plugin. The network is mocked."""

import io
import json
import urllib.error

import hermes_plugin_huntapi as plugin
import pytest
from hermes_plugin_huntapi import _client


class FakeContext:
    def __init__(self, settings=None):
        self.settings = settings or {}
        self.providers, self.tools = [], {}

    def get_config(self, key, default=None):
        return self.settings.get(key, default)

    def register_web_search_provider(self, provider):
        self.providers.append(provider)

    def register_tool(self, name, toolset, schema, handler, check_fn=None, **kwargs):
        self.tools[name] = {"toolset": toolset, "schema": schema, "handler": handler, "check_fn": check_fn}


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class Calls(list):
    """Records each request and answers it with the payload given to respond()."""

    def __init__(self, monkeypatch):
        super().__init__()
        self.monkeypatch = monkeypatch

    def respond(self, payload):
        def urlopen(request, timeout):
            self.append({"request": request, "timeout": timeout})
            return FakeResponse(json.dumps(payload).encode())

        self.monkeypatch.setattr(_client.urllib.request, "urlopen", urlopen)

    def fail(self, status, body):
        def urlopen(request, timeout):
            self.append({"request": request, "timeout": timeout})
            raise urllib.error.HTTPError(request.full_url, status, "error", {}, io.BytesIO(json.dumps(body).encode()))

        self.monkeypatch.setattr(_client.urllib.request, "urlopen", urlopen)

    def unreachable(self):
        def urlopen(request, timeout):
            raise urllib.error.URLError("down")

        self.monkeypatch.setattr(_client.urllib.request, "urlopen", urlopen)


@pytest.fixture
def calls(monkeypatch):
    return Calls(monkeypatch)


@pytest.fixture
def api_key(monkeypatch):
    monkeypatch.setattr(_client, "get_secret", lambda name, default=None: "test-key" if name == _client.KEY_ENV else default)


@pytest.fixture
def no_key(monkeypatch):
    monkeypatch.setattr(_client, "get_secret", lambda name, default=None: default)


def query(request):
    return dict(_client.urllib.parse.parse_qsl(_client.urllib.parse.urlsplit(request.full_url).query))


def assert_auth(request):
    assert request.get_header("User-agent").startswith("hermes-plugin-huntapi/")
    assert request.get_header("X-api-key") == "test-key"


def tools():
    ctx = FakeContext()
    plugin.register(ctx)
    return ctx.tools


def run(name, args):
    return json.loads(tools()[name]["handler"](args, task_id="t1"))


def test_register_declares_every_tool():
    registered = tools()
    assert sorted(registered) == sorted(['huntapi_media_metadata', 'huntapi_video_download', 'huntapi_audio_download', 'huntapi_job_status'])
    for name, tool in registered.items():
        assert tool["toolset"] == "huntapi"
        assert tool["schema"]["name"] == name
        assert tool["schema"]["parameters"]["type"] == "object"


def test_tools_hidden_without_key(no_key):
    assert all(tool["check_fn"]() is False for tool in tools().values())


def test_tools_shown_with_key(api_key):
    assert all(tool["check_fn"]() is True for tool in tools().values())


def test_missing_key_returns_an_error(no_key, calls):
    assert "HUNTAPI_API_KEY" in run('huntapi_media_metadata', {'url': 'https://www.youtube.com/watch?v=jNQXAC9IVRw'})["error"]
    assert calls == []


def test_missing_required_argument(api_key, calls):
    assert "required" in run('huntapi_media_metadata', {})["error"]
    assert calls == []


@pytest.mark.parametrize("name,args,url", [('huntapi_media_metadata', {'url': 'https://www.youtube.com/watch?v=jNQXAC9IVRw'}, 'https://api.huntapi.com/v1/media/metadata?query=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DjNQXAC9IVRw'), ('huntapi_video_download', {'url': 'https://www.youtube.com/watch?v=jNQXAC9IVRw', 'video_quality': '720', 'video_format': 'mp4'}, 'https://api.huntapi.com/v1/video/download?query=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DjNQXAC9IVRw&video_quality=720&video_format=mp4'), ('huntapi_audio_download', {'url': 'https://www.youtube.com/watch?v=jNQXAC9IVRw', 'audio_format': 'mp3'}, 'https://api.huntapi.com/v1/audio/download?query=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DjNQXAC9IVRw&audio_format=mp3'), ('huntapi_job_status', {'job_id': 'abc-123'}, 'https://api.huntapi.com/v1/jobs/abc-123')])
def test_each_tool_calls_its_endpoint(api_key, calls, name, args, url):
    calls.respond({"ok": True})
    assert run(name, args) == {"ok": True}
    request = calls[0]["request"]
    assert request.full_url == url
    assert request.get_method() == "GET"
    assert_auth(request)


def test_api_error_message_is_returned(api_key, calls):
    calls.fail(400, {'error': 'Invalid query'})
    assert run('huntapi_media_metadata', {'url': 'https://www.youtube.com/watch?v=jNQXAC9IVRw'}) == {"error": "HuntAPI: Invalid query"}


def test_network_error(api_key, calls):
    calls.unreachable()
    assert run('huntapi_media_metadata', {'url': 'https://www.youtube.com/watch?v=jNQXAC9IVRw'}) == {"error": "HuntAPI: could not reach the API"}
