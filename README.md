# CrewAI Blog Researcher

A multi-agent pipeline built with [CrewAI](https://github.com/crewAIInc/crewAI) that turns a topic into a short, sourced blog post. Three agents work in sequence: one researches the web, one writes the draft, and one edits it into a final article.

## How It Works

| Step | Agent | What it does |
|------|-------|--------------|
| 1 | **Content Researcher** | Searches the web (via Serper) and returns five key findings, each with a source URL |
| 2 | **Blog Writer** | Writes a 300–400 word post from those findings, keeping the source URLs |
| 3 | **Content Editor** | Polishes grammar, flow, and length, and returns only the final article |

The tasks run sequentially, and each one receives the previous task's output as context. The prompts tell the agents not to invent facts or references and to flag anything that can't be verified.

## Getting Started

**1. Install dependencies**

```bash
pip install -r requirements.txt
```

**2. Create a `.env` file** in the project root

```env
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-4o                           # model name (see note below)
OPENAI_API_BASE=https://api.openai.com/v1     # or any OpenAI-compatible endpoint
SERPER_API_KEY=your_serper_key                # from serper.dev, used for web search
```

If you use a non-OpenAI provider through a compatible endpoint, you may need to prefix the model name (for example `openai/your-model`), since CrewAI routes models through LiteLLM.

**3. Run**

```bash
python main.py
```

Enter a topic when prompted, for example `The future of quantum computing`. The agents' reasoning is printed as they work, followed by the final blog post.

## Project Structure

```
crewai-blog-researcher/
├── main.py            # Agents, tasks, and crew definition
├── requirements.txt
└── .gitignore
```

## Customization

- Change the article length, tone, or number of findings by editing the task descriptions in `main.py`.
- Adjust `temperature` in the `LLM(...)` call to make output more or less creative.
- Add more agents (for example a fact-checker or an SEO reviewer) and append their tasks to the crew.

## Tech Stack

Python · CrewAI · crewai-tools (SerperDevTool) · OpenAI-compatible API · python-dotenv
