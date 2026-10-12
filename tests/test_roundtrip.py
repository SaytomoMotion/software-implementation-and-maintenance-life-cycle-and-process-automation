import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ProcessTests(unittest.TestCase):
    def test_lifecycle_across_processes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = str(Path(directory) / "tasks.json")

            def run(*arguments):
                return subprocess.run([sys.executable, "-m", "tasktracker", "--data", path,
                                       *arguments], capture_output=True, text=True, check=False)

            self.assertEqual(run("add", "Read lecture 0").returncode, 0)
            listing = run("list", "--json")
            self.assertEqual(listing.returncode, 0)
            task = json.loads(listing.stdout)[0]
            self.assertEqual(run("complete", task["id"]).returncode, 0)
            self.assertTrue(json.loads(run("list", "--json").stdout)[0]["completed"])
            failed = run("complete", "invalid")
            self.assertEqual(failed.returncode, 1)
            self.assertNotIn("Traceback", failed.stderr)
