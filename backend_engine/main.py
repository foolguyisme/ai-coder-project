from __future__ import annotations

import logging
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend_engine.llm_server import LLMEngine
from src.config.settings import settings

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
  "You are an expert software engineer. Respond with clean, production-ready code "
  "and brief explanations when helpful."
)

app = FastAPI(
  title="AI Coder API",
  description="Local LLM-powered code generation service",
  version="1.0.0",
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_methods=["*"],
  allow_headers=["*"],
)

_engine: Optional[LLMEngine] = None


def get_engine() -> LLMEngine:
  global _engine
  if _engine is None:
    if not settings.model_path.exists():
      raise HTTPException(
        status_code=503,
        detail=f"Model not found at {settings.model_path}. Run scripts/download_model.py first.",
      )
    _engine = LLMEngine(
      model_path=str(settings.model_path),
      max_new_tokens=settings.max_new_tokens,
      temperature=settings.temperature,
    )
  return _engine


class GenerateRequest(BaseModel):
  prompt: str = Field(..., min_length=1, description="Coding task or snippet to complete")
  system_prompt: Optional[str] = Field(default=None, description="Optional system instruction override")


class GenerateResponse(BaseModel):
  output: str
  model_path: str


@app.get("/health")
def health_check() -> dict:
  return {
    "status": "ok",
    "model_path": str(settings.model_path),
    "model_exists": settings.model_path.exists(),
  }


@app.post("/generate", response_model=GenerateResponse)
def generate_code(request: GenerateRequest) -> GenerateResponse:
  try:
    engine = get_engine()
    output = engine.generate(
      prompt=request.prompt,
      system_prompt=request.system_prompt or SYSTEM_PROMPT,
    )
  except HTTPException:
    raise
  except Exception as exc:
    logger.exception("Generation failed")
    raise HTTPException(status_code=500, detail=str(exc)) from exc

  return GenerateResponse(output=output, model_path=str(settings.model_path))


if __name__ == "__main__":
  import uvicorn

  uvicorn.run("backend_engine.main:app", host=settings.host, port=settings.port, reload=False)
