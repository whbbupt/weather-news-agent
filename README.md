# Weather & News Agent

A single-purpose AI agent that answers weather and news queries using local LLM (Ollama) function calling. Built for course "软件产品综合开发实践 — 实验二 (BYOA)".

## Prerequisites

1. Install [Ollama](https://ollama.com/download)
2. Pull the model: `ollama pull qwen2.5:7b`
3. Ensure Ollama is running (`ollama serve` starts automatically on Windows)

## Install

```bash
pip install httpx feedparser
```

## Usage

```bash
python agent.py
```

Example queries:
- "北京今天天气怎么样？"
- "What's the weather in London?"
- "最近AI领域有什么新闻？"
- "Show me technology news"

## Project Structure

| File | Purpose |
|------|---------|
| `agent.py` | CLI main loop, conversation history management |
| `llm_client.py` | Ollama chat API wrapper with tool-calling orchestration |
| `tools.py` | Tool implementations: `get_weather` (Open-Meteo), `get_news` (domestic RSS) |
| `tool_schemas.py` | JSON Schema tool definitions for Ollama function calling |

## Architecture

```
User Input (CLI)
      |
      v
agent.py ──► Ollama (qwen2.5:7b) ──► tool_calls
      |                                    |
      |◄─────── text response ─────────────┘
      |
      v (execute tools)
tools.py ──► Open-Meteo API (weather)
        ──► IT之家 / 36氪 RSS (news)
```

## Context Integration

Uses **LLM Function Calling**: tool execution results are injected into the conversation context as `tool` role messages, enabling the LLM to synthesize natural-language responses from live external data. This matches the course requirement for "standard LLM function calling" or "MCP or similar" context integration.

## Data Sources

| Source | API | Cost |
|--------|-----|------|
| Open-Meteo | `https://api.open-meteo.com` | Free, no key |
| IT之家 RSS | `https://www.ithome.com/rss/` | Free, no key |
| 36氪 RSS | `https://36kr.com/feed` | Free, no key |
| 少数派 RSS | `https://sspai.com/feed` | Free, no key |
| OSChina RSS | `https://www.oschina.net/news/rss` | Free, no key |

All sources are accessible from within China without proxy.
