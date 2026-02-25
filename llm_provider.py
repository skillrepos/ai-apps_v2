#!/usr/bin/env python3
"""
Lab 6: LLM Provider — Unified interface for local and cloud models
═══════════════════════════════════════════════════════════════════════
Provides a single get_llm() function that returns the right LLM backend:

  - If HF_TOKEN is set  →  HuggingFace Inference API  (cloud / HF Spaces)
  - Otherwise           →  Ollama local model          (Codespaces / local)

Both backends expose the same .invoke(messages) interface, so the rest
of the application code doesn't need to know which one is running.
"""

import os

# ╔══════════════════════════════════════════════════════════════════╗
# ║ 1.  Configuration                                               ║
# ╚══════════════════════════════════════════════════════════════════╝
HF_MODEL = "meta-llama/Llama-3.1-8B-Instruct"


# ╔══════════════════════════════════════════════════════════════════╗
# ║ 2.  Response wrapper                                             ║
# ╚══════════════════════════════════════════════════════════════════╝
# TODO: HFResponse class that wraps HF responses to look like LangChain


# ╔══════════════════════════════════════════════════════════════════╗
# ║ 3.  HuggingFace Inference API wrapper                           ║
# ╚══════════════════════════════════════════════════════════════════╝
# TODO: HFLLMWrapper class with __init__ and invoke methods
#       - __init__ creates an InferenceClient from huggingface_hub
#       - invoke(messages) sends messages to HF API and returns HFResponse


# ╔══════════════════════════════════════════════════════════════════╗
# ║ 4.  Provider factory — returns the right LLM backend            ║
# ╚══════════════════════════════════════════════════════════════════╝
def get_llm():
    """
    Return an LLM instance based on the environment.

    - If HF_TOKEN is set → HuggingFace Inference API (for HF Spaces)
    - Otherwise          → Ollama local model         (for Codespaces)
    """
    # TODO: Check for HF_TOKEN and return the appropriate LLM backend


# ╔══════════════════════════════════════════════════════════════════╗
# ║ 5.  Quick self-test                                              ║
# ╚══════════════════════════════════════════════════════════════════╝
if __name__ == "__main__":
    print("=" * 50)
    print("LLM Provider — Self Test")
    print("=" * 50)
    llm = get_llm()
    print("\nSending test message...")
    response = llm.invoke([{"role": "user", "content": "Say hello in one sentence."}])
    print(f"Response: {response.content}")
