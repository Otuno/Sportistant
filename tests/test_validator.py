import unittest
from services.validator import Validator


class TestValidator(unittest.TestCase):
    """Unit tests for the Validator service."""

    def setUp(self):
        self.validator = Validator()

    def test_valid_team_names(self):
        """Test valid team names pass validation."""
        self.assertTrue(self.validator.is_valid_team_name("Arsenal"))
        self.assertTrue(self.validator.is_valid_team_name("Real Madrid"))
        self.assertTrue(self.validator.is_valid_team_name("AC Milan"))

    def test_invalid_team_names(self):
        """Test invalid or empty team names fail validation."""
        self.assertFalse(self.validator.is_valid_team_name(""))
        self.assertFalse(self.validator.is_valid_team_name("   "))

    def test_valid_notes(self):
        """Test valid note inputs."""
        self.assertTrue(self.validator.is_valid_note("Great match history."))
        self.assertTrue(self.validator.is_valid_note("Strong defensive record."))

    def test_invalid_notes(self):
        """Test empty notes fail validation."""
        self.assertFalse(self.validator.is_valid_note(""))
        self.assertFalse(self.validator.is_valid_note("   "))


if __name__ == "__main__":
    unittest.main()