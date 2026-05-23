import importlib.util
import unittest
from pathlib import Path
from unittest.mock import Mock, patch


def load_cli_module():
    script_path = next(Path(__file__).parents[1].glob("AUTOQAGPT_COMPARE*.py"))
    spec = importlib.util.spec_from_file_location("autoqallms_compare", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class GeminiProviderTests(unittest.TestCase):
    def test_generate_with_gemini_returns_generated_candidate_text(self):
        module = load_cli_module()
        module.GEMINI_API_KEY = "test-key"
        module.GEMINI_MODEL = "gemini-2.5-flash"
        response = Mock()
        response.json.return_value = {
            "candidates": [
                {"content": {"parts": [{"text": "print('generated')"}]}}
            ]
        }

        with patch.object(module.requests, "post", return_value=response) as post:
            generated = module.generate_with_gemini("selenium prompt")

        self.assertEqual(generated, "print('generated')")
        post.assert_called_once_with(
            "https://generativelanguage.googleapis.com/v1beta/models/"
            "gemini-2.5-flash:generateContent",
            params={"key": "test-key"},
            json={"contents": [{"parts": [{"text": "selenium prompt"}]}]},
            timeout=120,
        )
        response.raise_for_status.assert_called_once_with()

    def test_generate_selenium_code_routes_gemini_selection(self):
        module = load_cli_module()

        with patch.object(
            module,
            "generate_with_gemini",
            return_value="generated script",
        ) as generator:
            result = module.generate_selenium_code(
                "https://example.com",
                {"links": []},
                "gemini",
            )

        self.assertEqual(result, "generated script")
        generator.assert_called_once()


if __name__ == "__main__":
    unittest.main()
