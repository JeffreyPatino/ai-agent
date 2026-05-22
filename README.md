# AI Coding Agent (Gemini + Vertex AI)

A lightweight, tool-using Python agent built while following along with this YouTube course:
https://www.youtube.com/watch?v=YtHdaXuOAks

This repository demonstrates my understanding of agent flow design, function-calling, and safe local file operations.

## Why I Built This

I wanted a hands-on project that shows:
- how an LLM can reason over a user prompt,
- decide when to call tools,
- execute those tools in a controlled working directory,
- and continue the conversation with tool outputs until it can produce a final answer.

## What The Agent Can Do

The agent supports four tool functions:
- `get_files_info`: list files/directories and metadata
- `get_file_content`: read file contents
- `write_file`: write/update files
- `run_python_file`: run Python files with optional args

All tool paths are constrained to a configured working directory (`calculator/`) to reduce risk from arbitrary file access.

## Architecture (High-Level)

- `main.py`
  - initializes Gemini client (Vertex AI)
  - sends prompt + tool schemas
  - runs the function-calling loop
- `call_function.py`
  - dispatches model-requested tool calls to local Python functions
  - wraps responses back into tool-result messages
- `functions/*.py`
  - concrete tool implementations and schema declarations
- `calculator/`
  - sandbox working directory used by the tools

## Tech Stack

- Python 3.12+
- `google-genai`
- `python-dotenv`
- Vertex AI (Gemini model)

## Setup

1. Create and activate a virtual environment.
2. Install dependencies.
3. Add env vars in `.env` (copy from `.env.example`).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
```

Set these values in `.env`:
- `GOOGLE_CLOUD_PROJECT`
- `GOOGLE_CLOUD_LOCATION`

You also need authenticated GCP credentials locally (for Vertex AI).

## Run

Basic run:

```bash
python main.py "what files are in the root?"
```

Verbose run (token and tool-call visibility):

```bash
python main.py "what is in tests.py" --verbose
```

## Portfolio Notes / Learnings

Key takeaways from building this:
- Function-calling is powerful, but success depends heavily on tool schema quality and argument naming consistency.
- A looped agent workflow (`model -> tool call -> tool result -> model`) is straightforward to implement and easy to extend.
- Guardrails like working-directory path checks are essential for safe file tools.
- Small output-format choices (like newline handling) make a big difference in perceived quality.

## Current Scope

This is intentionally a focused learning project and not a production-ready framework.
Potential future improvements:
- stronger argument validation and normalization
- structured logging
- unit tests for each function module
- retry/backoff and model error handling improvements

## Repository Structure

```text
aiagent/
  main.py
  call_function.py
  config.py
  functions/
    get_files_info.py
    get_file_content.py
    write_file.py
    run_python_file.py
  calculator/
    main.py
    tests.py
    pkg/
      calculator.py
      render.py
```

## License

MIT (see `LICENSE`).

