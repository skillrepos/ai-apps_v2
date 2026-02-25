#!/usr/bin/env python3
"""
Lab 6: Self-Contained Office Agent (Deployable)
═══════════════════════════════════════════════════════════════════════
A deployable version of the RAG agent from Lab 5 that:
- Uses llm_provider for flexible LLM backend (Ollama OR HF Inference)
- Starts the MCP server as a SUBPROCESS via stdio transport
- Still uses ChromaDB for office RAG search (from Lab 4)
- Ready for Gradio interface (Lab 7) and HF deployment (Lab 8)

Tools Available to the Agent
----------------------------
1. search_offices(query) → text chunks from office vector DB (local RAG)
2. geocode_location(name) → lat/lon coordinates (MCP server)
3. get_weather(lat, lon)  → current weather in Celsius (MCP server)
4. convert_c_to_f(c)      → temperature in Fahrenheit (MCP server)

Key Differences from Lab 5's rag_agent.py
------------------------------------------
- Lab 5 connected to the MCP server over HTTP → requires running it
  separately with "python mcp_server.py"
- This version starts the MCP server as a SUBPROCESS and connects
  via stdio transport → fully self-contained, one command to run
- Lab 5 used ChatOllama directly → this uses llm_provider (Ollama or HF)
- Adds a synchronous wrapper so Gradio can call it easily
"""

# ────────────────────────── standard libs ───────────────────────────
import asyncio
import json
import re
import sys
import textwrap
from pathlib import Path

# ────────────────────────── third-party libs ────────────────────────
import chromadb
from chromadb.config import Settings, DEFAULT_TENANT, DEFAULT_DATABASE
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from fastmcp import Client
from mcp import StdioServerParameters

# ────────────────────────── our modules ─────────────────────────────
from llm_provider import get_llm

# ╔══════════════════════════════════════════════════════════════════╗
# ║ 1.  Configuration                                               ║
# ╚══════════════════════════════════════════════════════════════════╝
CHROMA_PATH     = Path("./chroma_db")
COLLECTION_NAME = "codebase"
TOP_K           = 3

# Regex patterns for parsing LLM responses (same as Labs 2, 3, and 5)
ACTION_RE = re.compile(r"Action:\s*(\w+)", re.IGNORECASE)
ARGS_RE   = re.compile(r"Args:\s*(\{.*?\})(?:\s|$)", re.S | re.IGNORECASE)

# MCP server subprocess configuration — starts mcp_server.py via stdio
# instead of connecting over HTTP. The wrapper runs the same FastMCP
# server but in stdio transport mode (stdin/stdout instead of HTTP).
MCP_SERVER = StdioServerParameters(
    command=sys.executable,
    args=["mcp_stdio_wrapper.py"],
)

# ╔══════════════════════════════════════════════════════════════════╗
# ║ 2.  RAG search tool (local — queries the ChromaDB from Lab 4)   ║
# ╚══════════════════════════════════════════════════════════════════╝
embed_fn = DefaultEmbeddingFunction()

def open_collection() -> chromadb.Collection:
    """Open the ChromaDB collection populated in Lab 4."""
    client = chromadb.PersistentClient(
        path=str(CHROMA_PATH),
        settings=Settings(),
        tenant=DEFAULT_TENANT,
        database=DEFAULT_DATABASE,
    )
    return client.get_or_create_collection(COLLECTION_NAME)

coll = open_collection()

def search_offices(query: str) -> str:
    """Search the office vector database for relevant information."""
    query_vec = embed_fn([query])[0]
    res = coll.query(
        query_embeddings=[query_vec],
        n_results=TOP_K,
        include=["documents"],
    )
    docs = res["documents"][0] if res["documents"] else []
    if not docs:
        return "No matching office information found."
    return "\n---\n".join(docs)

# ╔══════════════════════════════════════════════════════════════════╗
# ║ 3.  MCP result unwrapper (same as Lab 5)                        ║
# ╚══════════════════════════════════════════════════════════════════╝

# TODO: Implement unwrap(obj) — extracts plain Python values from
#       FastMCP result wrappers. Check for structured_content, data,
#       text (try JSON parse), value, single-element lists, and
#       single-numeric-value dicts. This is the same as Lab 5.

# ╔══════════════════════════════════════════════════════════════════╗
# ║ 4.  System prompt — tells the LLM about all available tools     ║
# ╚══════════════════════════════════════════════════════════════════╝
SYSTEM = textwrap.dedent("""
You are an office information agent. You answer questions about company
offices by searching a database and looking up live weather data.

You have these tools:

# TODO: Tool descriptions, response format, examples, and rules

""").strip()

# ╔══════════════════════════════════════════════════════════════════╗
# ║ 5.  Async TAO agent loop (starts MCP server via stdio)          ║
# ╚══════════════════════════════════════════════════════════════════╝
async def _run_agent_async(prompt: str, max_steps: int = 10) -> str:
    """
    Run the TAO agent loop with the MCP server as a subprocess.

    The MCP server is started via stdio transport — the agent spawns
    mcp_stdio_wrapper.py as a child process and talks MCP protocol
    over stdin/stdout. This is the standard production pattern.
    """
    llm = get_llm()

    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user",   "content": prompt},
    ]

    print("\n" + "=" * 60)
    print("Office Agent — Thought / Action / Observation")
    print("=" * 60 + "\n")

    # Start MCP server as subprocess and connect via stdio
    async with Client(MCP_SERVER) as mcp:
        for step in range(1, max_steps + 1):
            print(f"[Step {step}]")

            # TODO: Invoke the LLM, parse the Action and Args from the
            #       response, check for DONE, dispatch to the right tool
            #       (search_offices locally, everything else via MCP),
            #       and feed the observation back to the LLM.
            #
            #       Key patterns:
            #       - Local tool:  result = search_offices(**args)
            #       - MCP tools:   raw = await mcp.call_tool(action, args)
            #                      result = unwrap(raw)

            pass  # Remove this line after merging

    return "Reached maximum steps without completing."


# ╔══════════════════════════════════════════════════════════════════╗
# ║ 6.  Synchronous wrapper (for Gradio and command-line use)       ║
# ╚══════════════════════════════════════════════════════════════════╝
def run_agent(prompt: str, max_steps: int = 10) -> str:
    """
    Synchronous entry point that Gradio and the command line use.
    Wraps the async agent loop with asyncio.run().
    """
    return asyncio.run(_run_agent_async(prompt, max_steps))


# ╔══════════════════════════════════════════════════════════════════╗
# ║ 7.  Interactive loop                                             ║
# ╚══════════════════════════════════════════════════════════════════╝
if __name__ == "__main__":
    print("=" * 60)
    print("Office Agent (Deployable Version)")
    print("=" * 60)
    print("\nAsk about any office (e.g. 'Tell me about HQ')")
    print("Type 'exit' to quit\n")

    while True:
        prompt = input("User: ").strip()
        if prompt.lower() == "exit":
            print("Goodbye!")
            break
        if prompt:
            run_agent(prompt)
            print()
