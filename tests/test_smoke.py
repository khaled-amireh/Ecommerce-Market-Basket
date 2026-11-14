"""Syntax and import safety, without a historical CSV or display."""
import pathlib
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class SmokeTests(unittest.TestCase):
    def test_script_compiles(self):
        compile((ROOT / "ecommerce_market_basket.py").read_text(), "script", "exec")

    def test_import_has_no_workflow_side_effects(self):
        code = "import sys; sys.path.insert(0, sys.argv[1]); import ecommerce_market_basket"
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run([sys.executable, "-c", code, str(ROOT)], cwd=directory,
                                    capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            self.assertEqual(list(pathlib.Path(directory).iterdir()), [])
