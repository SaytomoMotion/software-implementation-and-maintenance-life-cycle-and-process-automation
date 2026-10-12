import unittest
from tasktracker.validation import validate_id, validate_title


class ValidationTests(unittest.TestCase):
    def test_trim_and_unicode(self):
        self.assertEqual(validate_title("  Read lecture 2  "), "Read lecture 2")
        self.assertEqual(validate_title("Study Latvijas vēsture"), "Study Latvijas vēsture")

    def test_invalid_titles(self):
        for title in ("", "   ", None, 23, "x" * 201, "hidden\nline", "hidden\x1bcode"):
            with self.subTest(title=title), self.assertRaises(ValueError):
                validate_title(title)

    def test_title_boundary(self):
        self.assertEqual(len(validate_title("x" * 200)), 200)

    def test_identifier(self):
        value = "12345678-1234-4234-8234-123456789abc"
        self.assertEqual(validate_id(value), value)
        for invalid in ("1", None, value.upper(), value.replace("-", "")):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                validate_id(invalid)
