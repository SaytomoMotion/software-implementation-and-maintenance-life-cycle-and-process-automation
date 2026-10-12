import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from tasktracker.cli import main


class CliTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.path = Path(self.folder.name) / "tasks.json"

    def invoke(self, *arguments):
        output, errors = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
            code = main(["--data", str(self.path), *arguments])
        return code, output.getvalue(), errors.getvalue()

    def test_empty_and_json_output(self):
        self.assertEqual(self.invoke("list"), (0, "No tasks found.\n", ""))
        self.assertEqual(json.loads(self.invoke("list", "--json")[1]), [])

    def test_add_complete_and_filter(self):
        self.assertEqual(self.invoke("add", "Study")[0], 0)
        record = json.loads(self.invoke("list", "--json")[1])[0]
        self.assertEqual(self.invoke("complete", record["id"])[0], 0)
        self.assertIn("[done] Study", self.invoke("list")[1])
        self.assertEqual(json.loads(self.invoke("list", "--status", "open", "--json")[1]), [])

    def test_invalid_title_and_id(self):
        for command in (("add", " "), ("complete", "invalid")):
            code, output, error = self.invoke(*command)
            self.assertEqual(code, 1)
            self.assertEqual(output, "")
            self.assertIn("Error:", error)
        self.assertFalse(self.path.exists())

    def test_corruption_is_reported_without_content(self):
        self.path.write_text("private invalid content", encoding="utf-8")
        code, _, errors = self.invoke("list")
        self.assertEqual(code, 1)
        self.assertNotIn("private invalid content", errors)
        self.assertNotIn("Traceback", errors)

    def test_argument_error_is_exit_two(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as caught:
            main(["list", "--status", "invalid"])
        self.assertEqual(caught.exception.code, 2)
