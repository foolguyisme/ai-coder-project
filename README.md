# AI Coder Project

> Local LLM-powered code generation platform with web UI, sandbox evaluation, and fine-tuning support.

**AI 程式碼助手平台** — 基於 Qwen2.5-Coder 的本地端程式碼生成、沙盒測試與微調訓練一站式解決方案。

---

## Overview

AI Coder Project is a full-stack local development assistant that wraps **Qwen2.5-Coder-7B-Instruct** behind a FastAPI backend and a lightweight web UI. Generated code can be validated in an isolated Docker sandbox, and models can be fine-tuned via LLaMA-Factory.

### Architecture

```
Hugging Face Model → FastAPI Backend → Web UI
                          ↓
                   Sandbox Evaluator (Docker)
                          ↓
                   LLaMA-Factory Fine-tuning
```

---

## Key Features

- **Local inference** — Run Qwen2.5-Coder-7B on your machine with GPU acceleration
- **REST API** — FastAPI endpoints for health checks and code generation
- **Web studio** — Clean browser UI for interactive prompting (Ctrl+Enter to submit)
- **Sandbox evaluation** — Isolated subprocess/Docker execution of generated code against test cases
- **Fine-tuning ready** — Pre-configured LLaMA-Factory YAML for LoRA SFT on code datasets
- **Modular layout** — Separated `backend_engine/`, `frontend_ui/`, `sandbox_eval/`, `training_env/`, `src/config/`

---

## Tech Stack

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688)
![Transformers](https://img.shields.io/badge/Transformers-Hugging%20Face-FFD21E)
![PyTorch](https://img.shields.io/badge/PyTorch-2.1+-EE4C2C?logo=pytorch&logoColor=white)
![Qwen](https://img.shields.io/badge/Qwen2.5--Coder-7B-6C5CE7)
![Docker](https://img.shields.io/badge/Docker-Sandbox-2496ED?logo=docker&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-Vanilla-F7DF1E?logo=javascript&logoColor=black)

---

## Project Structure

```
ai-coder-project/
├── backend_engine/     # FastAPI app + LLM inference engine
├── frontend_ui/        # Browser-based code assistant UI
├── sandbox_eval/       # Code evaluation sandbox (Docker)
├── training_env/       # LLaMA-Factory fine-tuning config
├── scripts/            # Model download utilities
└── src/config/         # Centralized application settings
```

---

## Getting Started

### 1. Install Dependencies

```bash
git clone https://github.com/foolguyisme/ai-coder-project.git
cd ai-coder-project
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r backend_engine/requirements.txt
```

### 2. Download Base Model (~15 GB)

```bash
python scripts/download_model.py
```

### 3. Start the API Server

```bash
python -m backend_engine.main
# API available at http://127.0.0.1:8000
# Docs at http://127.0.0.1:8000/docs
```

### 4. Open the Web UI

Serve `frontend_ui/index.html` with any static file server, or open it directly in a browser while the API is running.

### 5. Evaluate Generated Code (Optional)

```bash
cd sandbox_eval
docker compose up --build
```

### 6. Fine-tune (Optional)

Configure `training_env/train_config.yaml` and run via [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory).

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MODEL_PATH` | `models/base_qwen_7b` | Path to downloaded model |
| `API_HOST` | `127.0.0.1` | FastAPI bind host |
| `API_PORT` | `8000` | FastAPI bind port |
| `MAX_NEW_TOKENS` | `512` | Max generation length |
| `TEMPERATURE` | `0.2` | Sampling temperature |

---

## License

MIT License — see repository for details.
