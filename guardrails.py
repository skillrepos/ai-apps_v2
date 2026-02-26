#!/usr/bin/env python3
"""
Guardrails — lightweight prompt-injection detection
═══════════════════════════════════════════════════════════════════════
Simple regex-based checks applied at three boundaries:

1. check_input()       — scan user prompts before the LLM sees them
2. check_tool_result() — scan MCP / RAG results before feeding to LLM
3. check_output()      — sanitise the final answer before the user sees it

This is NOT a bulletproof solution — production apps layer multiple
defences (embedding classifiers, LLM-based judges, allow-lists, etc.).
But even basic regex checks stop the most common injection attempts
and illustrate the "defence in depth" principle.
"""

import re
import logging
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)

# ── Security log file — appended to on every detection ─────────────
SECURITY_LOG = Path(__file__).parent / "security.log"

def _log_security_event(event_type: str, detail: str, matched: list[str]):
    """Append a timestamped entry to the security log file."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(SECURITY_LOG, "a") as f:
        f.write(f"[{timestamp}] {event_type} | patterns={matched} | {detail}\n")

# ╔══════════════════════════════════════════════════════════════════╗
# ║ 1.  Injection patterns                                          ║
# ╚══════════════════════════════════════════════════════════════════╝

INJECTION_PATTERNS = [
    re.compile(r"ignore\s+(all\s+)?previous\s+instructions", re.I),
    re.compile(r"ignore\s+(all\s+)?above\s+instructions", re.I),
    re.compile(r"disregard\s+(all\s+)?(previous|prior|above)", re.I),
    re.compile(r"you\s+are\s+now\s+(a|an)\s+", re.I),
    re.compile(r"new\s+instructions?\s*:", re.I),
    re.compile(r"system\s*:\s*", re.I),
    re.compile(r"<\s*system\s*>", re.I),
    re.compile(r"pretend\s+(you\s+are|to\s+be)", re.I),
    re.compile(r"override\s+(your\s+)?(instructions|rules|prompt)", re.I),
    re.compile(r"forget\s+(your|all)\s+(instructions|rules|training)", re.I),
    re.compile(r"do\s+not\s+follow\s+(your|the)\s+(rules|instructions)", re.I),
    re.compile(r"jailbreak", re.I),
]

# ╔══════════════════════════════════════════════════════════════════╗
# ║ 2.  Scanner helper                                               ║
# ╚══════════════════════════════════════════════════════════════════╝

def scan_text(text: str) -> list[str]:
    """Scan text for prompt injection patterns.

    Returns a list of matched pattern strings (empty if clean).
    """
    matches = []
    for pattern in INJECTION_PATTERNS:
        if pattern.search(text):
            matches.append(pattern.pattern)
    return matches

# ╔══════════════════════════════════════════════════════════════════╗
# ║ 3.  Input check                                                  ║
# ╚══════════════════════════════════════════════════════════════════╝

def check_input(prompt: str) -> tuple[bool, str]:
    """Check user input for injection attempts.

    Returns:
        (True,  original_prompt)  — if clean
        (False, refusal_message)  — if injection detected
    """
    matches = scan_text(prompt)
    if matches:
        logger.warning(f"⚠️  Input injection detected: {matches}")
        _log_security_event("INPUT_BLOCKED", f"prompt={prompt!r:.200}", matches)
        return False, "I can only answer questions about office locations and weather."
    return True, prompt

# ╔══════════════════════════════════════════════════════════════════╗
# ║ 4.  Tool-result check                                            ║
# ╚══════════════════════════════════════════════════════════════════╝

def check_tool_result(tool_name: str, result: str) -> tuple[bool, str]:
    """Check MCP / RAG tool results for injected instructions.

    If suspicious content is found it is replaced with [FILTERED]
    so the LLM never sees the raw injection text.

    Returns:
        (True,  original_text)   — if clean
        (False, sanitised_text)  — if injection detected and scrubbed
    """
    text = str(result)
    matches = scan_text(text)
    if matches:
        logger.warning(f"⚠️  Injection in {tool_name} result: {matches}")
        _log_security_event("TOOL_SANITISED", f"tool={tool_name}", matches)
        for pattern in INJECTION_PATTERNS:
            text = pattern.sub("[FILTERED]", text)
        return False, text
    return True, text

# ╔══════════════════════════════════════════════════════════════════╗
# ║ 5.  Output check                                                 ║
# ╚══════════════════════════════════════════════════════════════════╝

def check_output(response: str) -> str:
    """Sanitise the final response before it reaches the user.

    Strips any injection-like phrases that might have leaked through
    the LLM's output (e.g. echoed back from a poisoned RAG chunk).
    """
    matches = scan_text(response)
    if matches:
        logger.warning(f"⚠️  Output contains suspicious patterns: {matches}")
        _log_security_event("OUTPUT_SANITISED", "final response", matches)
        for pattern in INJECTION_PATTERNS:
            response = pattern.sub("[FILTERED]", response)
    return response
