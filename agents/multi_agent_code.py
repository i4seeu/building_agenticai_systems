from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

try:
	from crewai import Agent, Task, Crew, Process
except Exception:
	# If crewai isn't installed in the environment, raise a clear error
	raise

def setup_environment() -> None:
	"""Load environment variables and ensure `GOOGLE_API_KEY` is set.

	Raises:
		ValueError: if `GOOGLE_API_KEY` is not found in the environment.
	"""
	load_dotenv('../.env')
	# if not os.getenv("GOOGLE_API_KEY"):
	# 	raise ValueError(
	# 		"GOOGLE_API_KEY not found. Please set it in your .env file."
	# 	)


def main() -> None:
	"""Initialize and run a small multi-agent crew to create a blog post.

	This example uses the `crewai` abstractions (Agent/Task/Crew) and an
	LLM wrapper (here `ChatOpenAI`). It focuses on the
	high-level control flow and correct Python structure so it can be run
	directly in the user's virtual environment after installing the
	required dependencies.
	"""
	setup_environment()

	# Define the language model to use. Pick an appropriate Gemini model
	# available to your Google Cloud project.
	llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.7)
	print("Language Model initialized")

	# Define Agents with specific roles and goals.
	researcher = Agent(
		role="Senior Research Analyst",
		goal="Find and summarize the latest trends in AI.",
		backstory=(
			"You are an experienced research analyst with a knack for "
			"identifying key trends and synthesizing information."
		),
		verbose=True,
		allow_delegation=False,
	)

	writer = Agent(
		role="Technical Content Writer",
		goal=(
			"Write a clear and engaging blog post based on research "
			"findings."
		),
		backstory=(
			"You are a skilled writer who can translate complex technical "
			"topics into accessible content."
		),
		verbose=True,
		allow_delegation=False,
	)

	# Define Tasks for the agents
	research_task = Task(
		description=(
			"Research the top 3 emerging trends in Artificial Intelligence "
			"in 2024-2025. Focus on practical applications and potential impact."
		),
		expected_output=(
			"A detailed summary of the top 3 AI trends, including key "
			"points and sources."
		),
		agent=researcher,
	)

	writing_task = Task(
		description=(
			"Write a 500-word blog post based on the research findings. The "
			"post should be engaging and easy for a general audience to understand."
		),
		expected_output="A complete 500-word blog post about the latest AI trends.",
		agent=writer,
		context=[research_task],
	)

	# Create the Crew. Use a sequential process so research runs before writing.
	blog_creation_crew = Crew(
		agents=[researcher, writer],
		tasks=[research_task, writing_task],
		process=Process.sequential,
		llm=llm,
		verbose=True,
	)

	# Execute the Crew and print results.
	print("## Running the blog creation crew with Gemini 2.0 Flash... ##")
	try:
		result = blog_creation_crew.kickoff()
		print("\n------------------\n")
		print("## Crew Final Output ##")
		print(result)
	except Exception as e:
		print(f"\nAn unexpected error occurred: {e}")


if __name__ == "__main__":
	main()