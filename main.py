
import os

from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool

load_dotenv()

llm = LLM(
    model=os.getenv("OPENAI_MODEL"),
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.2
)

search_tool = SerperDevTool()

researcher = Agent(
    role="Content Researcher",
    goal="Find accurate, relevant, and up-to-date information about {topic}.",
    backstory=(
        "You are an experienced researcher who identifies reliable sources, "
        "checks factual claims, and extracts useful insights."
    ),
    tools=[search_tool],
    llm=llm,
    verbose=True,
)

writer = Agent(
    role="Blog Writer",
    goal="Write an engaging and informative blog post about {topic}.",
    backstory=(
        "You are a professional technology writer who turns research findings "
        "into clear, well-structured articles for a general audience."
    ),
    llm=llm,
    verbose=True,
)

editor = Agent(
    role="Content Editor",
    goal="Improve the accuracy, clarity, structure, and readability of the blog post.",
    backstory=(
        "You are a meticulous editor who checks factual consistency, removes "
        "repetition, improves transitions, and preserves source references."
    ),
    llm=llm,
    verbose=True,
)

research_task = Task(
    description=(
        "Research the topic: {topic}. Use web search to identify five key findings. "
        "For each finding, provide a concise explanation and its source URL. "
        "Prefer reliable and recent sources. Do not invent facts or references. "
        "Clearly identify any information that cannot be verified."
    ),
    expected_output=(
        "Five numbered research findings, each supported by a source URL, "
        "followed by a short list of the most useful sources."
    ),
    agent=researcher,
)

writing_task = Task(
    description=(
        "Write a 300–400 word blog post about {topic} using the research task's "
        "findings. Include an engaging title, introduction, organized body, "
        "and conclusion. Preserve source URLs for factual claims. "
        "Do not introduce unsupported facts."
    ),
    expected_output=(
        "A complete 300–400 word blog post with a title, introduction, "
        "body, conclusion, and relevant source URLs."
    ),
    agent=writer,
    context=[research_task],
)

editing_task = Task(
    description=(
        "Review and edit the draft produced by the writer. Improve grammar, "
        "clarity, flow, and consistency. Check that the article follows the "
        "requested length and retains its source URLs. Do not add unsupported "
        "claims. Return only the final revised article."
    ),
    expected_output="A polished, publication-ready blog post with source URLs.",
    agent=editor,
    context=[writing_task],
)

crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, writing_task, editing_task],
    process=Process.sequential,
    verbose=True,
)

if __name__ == "__main__":
    topic = input("Enter a blog topic: ").strip()

    if not topic:
        raise ValueError("Topic cannot be empty.")

    result = crew.kickoff(inputs={"topic": topic})

    print("\n")
    print("FINAL BLOG POST")
    print(result)
