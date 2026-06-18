# Weather & News Agent

A single-purpose AI agent that answers weather and news queries using local LLM (Ollama) function calling. Built for course "软件产品综合开发实践 — 实验二 (BYOA)".

## Quick Start

```bash
git clone https://github.com/whbbupt/weather-news-agent.git
cd weather-news-agent
pip install -r requirements.txt
ollama pull qwen2.5:7b
python agent.py
```

If Ollama is not running, open the Ollama desktop app or run:

```bash
ollama serve
```

## Usage

After starting the agent, ask questions such as:

```text
>>> What's the weather in Beijing?
>>> How is the weather in Ulaanbaatar?
>>> Show me recent AI news
>>> What's the weather in Shanghai? Also show me open-source news.
```

Type `quit` or `exit` to stop the agent.

## Project Structure

| File | Purpose |
|------|---------|
| `agent.py` | CLI main loop, conversation history management |
| `llm_client.py` | Ollama chat API wrapper with tool-calling orchestration |
| `tools.py` | Tool implementations: `get_weather` (Open-Meteo), `get_news` (domestic RSS) |
| `tool_schemas.py` | JSON Schema tool definitions for Ollama function calling |
| `requirements.txt` | Python dependency list for quick installation |

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
