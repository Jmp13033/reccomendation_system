from langchain_google_genai import ChatGoogleGenerativeAI
from crewai import Agent, Crew, Task, Process
from crewai_tools import SerperDevTool
from dotenv import load_dotenv, find_dotenv
import os 
load_dotenv()

search_tool = SerperDevTool()

llm = ChatGoogleGenerativeAI(model="gemini-pro",
                             google_api_key="AIzaSyCeVPr2cIFHPLixcU0AvLFN688q_7mfl0U"
                             )





# Define the research agent
research_agent = Agent(
    goal="To conduct thorough research on various topics and provide a comprehensive list of information about {book_title}",
    role="Researcher",
    backstory="Having a passion for gathering knowledge and presenting it in an organized manner.",
    llm=llm,
    verbose=True
)

# Define the write agent
write_agent = Agent(
    goal="To create engaging and informative content based on research findings from {book_title}.",
    role="Writer",
    backstory="With a background in writing and a knack for crafting compelling narratives.",
    llm=llm, 
    verbose=True
)

# Define the research task
research_task = Task(
    description="Research the topic {book_title} book and provide a comprehensive list of information.",
    expected_output="A comprehensive list of information about the {book_title}.",
    tools=[search_tool],
    agent=research_agent
)

# Define the writing task
write_task = Task(
    description=(
        "Compose a brief summary of the book '{book_title}'."
    ),
    expected_output="Two concise summaries: one for the book and another for why readers would enjoy these books.",
    agent=write_agent,
    async_execution=False, 
    tools=[search_tool]
)

# Define the crew with the agents and tasks
crew = Crew(
    agents=[research_agent, write_agent],
    tasks=[research_task, write_task],
    process=Process.sequential,
)

# Start the task execution process with enhanced feedback
result = crew.kickoff(inputs={'book_title': "Twilight"})

# Print the result
print(result)
