from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class LLMEngine:
  """Thin wrapper around a Hugging Face causal LM for code generation."""

  def __init__(self, model_path: str, max_new_tokens: int = 512, temperature: float = 0.2):
    self.model_path = model_path
    self.max_new_tokens = max_new_tokens
    self.temperature = temperature
    self._tokenizer = None
    self._model = None

  def _ensure_loaded(self) -> None:
    if self._model is not None:
      return
    try:
      from transformers import AutoModelForCausalLM, AutoTokenizer
      import torch
    except ImportError as exc:
      raise RuntimeError(
        "transformers and torch are required. Install backend_engine/requirements.txt"
      ) from exc

    logger.info("Loading model from %s", self.model_path)
    self._tokenizer = AutoTokenizer.from_pretrained(self.model_path, trust_remote_code=True)
    self._model = AutoModelForCausalLM.from_pretrained(
      self.model_path,
      device_map="auto",
      torch_dtype=torch.float16,
      trust_remote_code=True,
    )

  def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
    """Generate code completion for the given prompt."""
    self._ensure_loaded()

    messages = []
    if system_prompt:
      messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    text = self._tokenizer.apply_chat_template(
      messages,
      tokenize=False,
      add_generation_prompt=True,
    )
    inputs = self._tokenizer(text, return_tensors="pt").to(self._model.device)

    outputs = self._model.generate(
      **inputs,
      max_new_tokens=self.max_new_tokens,
      temperature=self.temperature,
      do_sample=self.temperature > 0,
    )
    generated = outputs[0][inputs["input_ids"].shape[-1] :]
    return self._tokenizer.decode(generated, skip_special_tokens=True).strip()
