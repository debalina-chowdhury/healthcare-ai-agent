[![CI](https://github.com/debalina-chowdhury/healthcare-ai-agent/actions/workflows/python-app.yml/badge.svg)](https://github.com/debalina-chowdhury/healthcare-ai-agent/actions)
# 🏥 Healthcare AI Agent

An AI-powered clinical assistant built with Anthropic's Claude API and Streamlit. The agent takes natural language queries about patients and autonomously decides which tools to call — looking up records, checking insurance, and scheduling appointments.

## How It Works

The agent uses Claude's native tool use API to reason through clinical queries:
1. Receives a natural language query
2. Decides which tools to call
3. Executes the tools and observes results
4. Synthesizes a natural language response

## Tools

- `search_patient_records` — Look up appointment history by patient ID
- `check_insurance` — Verify insurance status and coverage dates
- `schedule_appointment` — Book appointments with specialty and preferred day

## Tech Stack

- Anthropic Claude (claude-sonnet-4-5)
- Streamlit
- Python 3.9

## Setup

```bash
pip install -r requirements.txt
echo "ANTHROPIC_API_KEY=your-key-here" > .env
streamlit run app.py
```

## Author

Debalina Chowdhury
