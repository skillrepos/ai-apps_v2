#!/usr/bin/env python3
"""
Starts the MCP weather server using stdio transport (for subprocess use).

Lab 3's mcp_server.py normally runs as an HTTP server. This tiny wrapper
imports the same server and runs it over stdio instead, so hf_agent.py
can start it as a subprocess — no network port required.

This is the standard way to embed an MCP server in a deployment:
the agent spawns it as a child process and talks MCP over stdin/stdout.
"""

from mcp_server import mcp

mcp.run(transport="stdio")
