import types
from cli_ai.api_client import ApiClient


def test_health_check(monkeypatch):
	client = ApiClient.__new__(ApiClient)
	client.api_key = "test"
	def mock_configure(api_key):
		return None
	class MockModel:
		def generate_content(self, prompt, generation_config=None, stream=False):
			return types.SimpleNamespace(text="ok")
	def mock_generate(model, *a, **k):
		return MockModel()
	def mock_embed_content(model, content):
		return {"embedding": [0.1, 0.2, 0.3]}
	import google.generativeai as genai
	monkeypatch.setattr(genai, "configure", mock_configure)
	monkeypatch.setattr(genai, "GenerativeModel", lambda m: MockModel())
	monkeypatch.setattr(genai, "embed_content", mock_embed_content)
	# init manually
	ApiClient.__init__(client, api_key="test", model="foo", embedding_model="bar")
	assert client.health_check() is True 