import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "external_submission_v1"


class ExternalSubmissionV1SmokeTests(unittest.TestCase):
    def test_release_readiness_summary_passes(self):
        r = subprocess.run(
            [sys.executable, str(KIT / "publish_gate" / "RELEASE_READINESS_SUMMARY.py")],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("external_action_performed=false", r.stdout)


if __name__ == "__main__":
    unittest.main()
