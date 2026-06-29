"""Download the base Qwen2.5-Coder model from Hugging Face Hub."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)

DEFAULT_REPO = "Qwen/Qwen2.5-Coder-7B-Instruct"
DEFAULT_OUTPUT = Path("models/base_qwen_7b")


def download_model(repo_id: str, output_dir: Path) -> None:
  try:
    from huggingface_hub import snapshot_download
  except ImportError as exc:
    raise RuntimeError("Install dependencies: pip install -r requirements.txt") from exc

  output_dir.mkdir(parents=True, exist_ok=True)
  logger.info("Downloading %s (~15 GB). This may take a while...", repo_id)

  snapshot_download(
    repo_id=repo_id,
    local_dir=str(output_dir),
    local_dir_use_symlinks=False,
  )
  logger.info("Model saved to %s", output_dir.resolve())


def main() -> None:
  parser = argparse.ArgumentParser(description="Download Qwen2.5-Coder base model")
  parser.add_argument("--repo-id", default=DEFAULT_REPO)
  parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
  args = parser.parse_args()

  try:
    download_model(args.repo_id, args.output)
  except Exception as exc:
    logger.error("Download failed: %s", exc)
    sys.exit(1)


if __name__ == "__main__":
  main()
