from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def run_python_test(code: str, test_code: str, timeout_sec: int = 30) -> dict:
  """Execute generated code with test assertions in an isolated subprocess."""
  with tempfile.TemporaryDirectory() as tmp_dir:
    solution_path = Path(tmp_dir) / "solution.py"
    test_path = Path(tmp_dir) / "test_solution.py"

    solution_path.write_text(code, encoding="utf-8")
    test_path.write_text(
      f"from solution import *\n\n{test_code}",
      encoding="utf-8",
    )

    try:
      result = subprocess.run(
        [sys.executable, str(test_path)],
        capture_output=True,
        text=True,
        timeout=timeout_sec,
        cwd=tmp_dir,
      )
      return {
        "passed": result.returncode == 0,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode,
      }
    except subprocess.TimeoutExpired:
      return {"passed": False, "stdout": "", "stderr": "Execution timed out", "returncode": -1}


def main() -> None:
  parser = argparse.ArgumentParser(description="Evaluate generated code against test cases")
  parser.add_argument("--code-file", required=True, help="Path to generated code")
  parser.add_argument("--test-file", required=True, help="Path to test assertions")
  parser.add_argument("--timeout", type=int, default=30)
  args = parser.parse_args()

  code = Path(args.code_file).read_text(encoding="utf-8")
  test_code = Path(args.test_file).read_text(encoding="utf-8")

  outcome = run_python_test(code, test_code, timeout_sec=args.timeout)
  print(json.dumps(outcome, indent=2))
  sys.exit(0 if outcome["passed"] else 1)


if __name__ == "__main__":
  main()
