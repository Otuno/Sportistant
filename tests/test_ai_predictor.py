import os
import tempfile
import unittest

from services.ai_predictor import AIPredictor


class DummySuccessfulGemini:
    def generate_response(self, prompt):
        return "Chelsea are in strong form."


class DummyEmptyGemini:
    def generate_response(self, prompt):
        return None


class DummyBrokenGemini:
    def generate_response(self, prompt):
        raise RuntimeError("Gemini API failed")


class TestAIPredictor(unittest.TestCase):
    def setUp(self):
        self.original_cwd = os.getcwd()
        self.temp_dir = tempfile.TemporaryDirectory()
        os.chdir(self.temp_dir.name)

    def tearDown(self):
        os.chdir(self.original_cwd)
        self.temp_dir.cleanup()

    def test_successful_response_is_logged(self):
        predictor = AIPredictor(DummySuccessfulGemini())

        response = predictor.generate_ai_insight(
            "Chelsea",
            ["W", "W", "D"],
            {"prediction": "Likely to win"},
        )

        self.assertEqual(response, "Chelsea are in strong form.")

        with open("data/ai_responses.log", "r", encoding="utf-8") as file:
            log_content = file.read()

        self.assertIn("Chelsea", log_content)
        self.assertIn("Chelsea are in strong form.", log_content)
        self.assertIn("Likely to win", log_content)

    def test_none_response_returns_fallback_and_logs_error(self):
        predictor = AIPredictor(DummyEmptyGemini())

        response = predictor.generate_ai_insight(
            "Chelsea",
            ["L", "D"],
            {"prediction": "Likely to lose"},
        )

        self.assertIn("AI insight is currently unavailable", response)

        with open("data/ai_errors.log", "r", encoding="utf-8") as file:
            log_content = file.read()

        self.assertIn("Chelsea", log_content)
        self.assertIn("Gemini was unable to return response", log_content)

    def test_gemini_error_returns_fallback_and_logs_error(self):
        predictor = AIPredictor(DummyBrokenGemini())

        response = predictor.generate_ai_insight(
            "Manchester City",
            ["W", "L"],
            {"prediction": "Competitive"},
        )

        self.assertIn("AI insight is currently unavailable", response)

        with open("data/ai_errors.log", "r", encoding="utf-8") as file:
            log_content = file.read()

        self.assertIn("Manchester City", log_content)
        self.assertIn("Gemini API failed", log_content)


if __name__ == "__main__":
    unittest.main()
