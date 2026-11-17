"""Exercise helper CLIs only in disposable local fixtures; no LLM required."""

import json
import os
import shlex
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[2] / "skills/systematic-debugging/scripts"


class HelperContracts(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="debug helper fixtures ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def run_helper(self, name, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPTS / name), *args],
            cwd=self.root,
            text=True,
            capture_output=True,
            timeout=20,
            check=False,
        )

    def repeat(self, code, *options):
        return self.run_helper(
            "repeat-run.py",
            "--runs",
            "4",
            "--json",
            *options,
            "--",
            sys.executable,
            "-c",
            code,
        )

    def test_repeat_parallel_indexed_failures(self):
        r = self.repeat(
            "import os; raise SystemExit(int(os.environ['REPEAT_RUN_INDEX']) % 2)",
            "--parallel",
            "2",
        )
        self.assertEqual(r.returncode, 1)
        data = json.loads(r.stdout)
        self.assertEqual(
            (data["runs_executed"], data["passed"], data["failed"]), (4, 2, 2)
        )
        self.assertEqual(data["failure_rate"], 0.5)

    def test_repeat_pass(self):
        r = self.repeat("pass")
        self.assertEqual(r.returncode, 0)
        self.assertEqual(json.loads(r.stdout)["passed"], 4)

    def test_repeat_stop(self):
        r = self.repeat("raise SystemExit(3)", "--stop-on-fail")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(json.loads(r.stdout)["runs_executed"], 1)

    def test_repeat_timeout(self):
        r = self.run_helper(
            "repeat-run.py",
            "--runs",
            "1",
            "--json",
            "--timeout",
            ".2",
            "--",
            sys.executable,
            "-c",
            "import time; time.sleep(5)",
        )
        self.assertEqual(r.returncode, 1)
        self.assertEqual(json.loads(r.stdout)["timed_out"], 1)

    def test_repeat_usage_and_start_error(self):
        for args in (
            ("--runs", "0", "--", sys.executable, "-c", "pass"),
            ("--runs", "1", "--", "nonexistent-debug-fixture-command"),
        ):
            self.assertEqual(self.run_helper("repeat-run.py", *args).returncode, 2)

    def pollute(self, *args):
        script = self.root / "runner.py"
        script.write_text(
            "from pathlib import Path\nimport sys\nif sys.argv[1]=='dirty': Path('pollution').write_text('evidence')\nraise SystemExit(7)\n",
            encoding="utf-8",
        )
        return self.run_helper(
            "find-polluter.py",
            "--cwd",
            str(self.root),
            *args,
            "--",
            sys.executable,
            str(script),
            "{test}",
        )

    def test_polluter_detects_and_retains_evidence(self):
        r = self.pollute(
            "--pollution-path", "pollution", "--test", "clean", "--test", "dirty"
        )
        self.assertEqual(r.returncode, 1)
        self.assertIn("polluter: dirty", r.stdout)
        self.assertEqual((self.root / "pollution").read_text(), "evidence")

    def test_polluter_clean_despite_failed_runner(self):
        r = self.pollute("--pollution-path", "pollution", "--test", "clean")
        self.assertEqual(r.returncode, 0)
        self.assertIn("runner exit code: 7", r.stdout)

    def test_polluter_rejects_initial_pollution(self):
        (self.root / "pollution").write_text("existing")
        r = self.pollute("--pollution-path", "pollution", "--test", "dirty")
        self.assertEqual(r.returncode, 2)
        self.assertEqual((self.root / "pollution").read_text(), "existing")

    def test_quoted_check_command(self):
        check = self.root / "clean check.py"
        check.write_text("raise SystemExit(0)\n")
        argv = [sys.executable, str(check)]
        command = subprocess.list2cmdline(argv) if os.name == "nt" else shlex.join(argv)
        r = self.pollute("--check-command", command, "--test", "clean")
        self.assertEqual(r.returncode, 0, r.stderr + r.stdout)

    def test_polluter_missing_runner(self):
        r = self.run_helper(
            "find-polluter.py",
            "--pollution-path",
            "pollution",
            "--test",
            "clean",
            "--",
            "nonexistent-debug-fixture-command",
            "{test}",
        )
        self.assertEqual(r.returncode, 2)


if __name__ == "__main__":
    unittest.main()
