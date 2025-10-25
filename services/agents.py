from crewai import Agent, LLM, Crew, Task
import os
from dotenv import load_dotenv
load_dotenv()

# You can set your API keys in environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ----------------------------
# LLM Instances
# ----------------------------
# Main LLM for token data analysis
llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    temperature=0.3,
    api_key=OPENAI_API_KEY
)

# Optional: Additional LLMs if needed
llm_groq = LLM(
    model="groq/llama3-8b-8192",
    temperature=0.3,
    api_key=GROQ_API_KEY
)

# ----------------------------
# Agent: Moralis Token Analyzer
# ----------------------------
moralis_analyzer = Agent(
    role="Moralis Token Analyzer",
    goal="Analyze the cryptocurrency token data {data} from Moralis and provide insights on price trends, liquidity, volume, and market activity.",
    backstory="An expert in blockchain and cryptocurrency analytics. Able to provide actionable insights on token metrics.",
    verbose=True,
    llm=llm
)

# ----------------------------
# Task: Analyze Token Data
# ----------------------------
moralis_analysis_task = Task(
    description="Analyze token data fetched from Moralis and generate a detailed report.",
    agent=moralis_analyzer,
    goal="Generate a detailed analysis of the token data {data}, covering price, liquidity, trading volume, and any key insights.",
    expected_output="moralis_token_analysis.md"
)

# ----------------------------
# Crew: Runs the Task
# ----------------------------
moralis_crew = Crew(
    agents=[moralis_analyzer],
    tasks=[moralis_analysis_task],
    verbose=True,
    memory=True
)