# EventFlow AI

An AI-assisted event management workspace for concerts, club nights, conferences, festivals and screenings.

## Features
- Six specialist assistants and a project manager
- Event brief, multilingual AI drafts, venue enquiries, schedules and marketing
- Deterministic EUR budget calculator, break-even tickets and CSV exports
- Session-based task tracking and daily brief
- Offline English template demo without API keys

## Run locally
Use Python 3.10 or newer.

```bash
python -m venv .venv
pip install -r requirements.txt
streamlit run app.py
```

Activate the virtual environment before installing dependencies (Windows: .venv\Scripts\activate; macOS/Linux: source .venv/bin/activate).

## AI configuration
Enter your own OpenAI API key in the password field or set the OPENAI_API_KEY environment variable. Optional OPENAI_MODEL overrides the default gpt-4o-mini. API usage may cost money. Never commit credentials. Event details are sent to the API when AI mode is used; avoid confidential or personal information.

## Deploy
On https://share.streamlit.io/ connect your GitHub account, select this repository, branch main and entry point app.py. The demo works without credentials. Users may enter their own API keys in the app.

## Repository inspiration
- [Awesome LLM Apps](https://github.com/shubhamsaboo/awesome-llm-apps): LLM application and specialist agent patterns.
- [AI Employees](https://github.com/markfulton/ai-employees): role-based business assistants and project coordination.

This is an original lightweight implementation inspired by those projects, not a fork or direct integration. Each specialist is a role-based LLM call, not a fully autonomous agent. Google Sheets CSV export and daily brief download are manual; automatic email, persistent database and live venue lookup are future extensions. Forecasts are illustrative, and no bookings or payments are made.
