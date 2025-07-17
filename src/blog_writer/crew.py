from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from blog_writer.storage import BlogStorage


@CrewBase
class BlogWriter():
    """BlogWriter crew for generating blog posts using AI agents."""

    agents: List[BaseAgent]
    tasks: List[Task]
    storage: BlogStorage

    def __init__(self, storage_dir: str = "blogs"):
        """Initialize the BlogWriter with storage system."""
        super().__init__()
        self.storage = BlogStorage(storage_dir)
        self.current_topic = None

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'], # type: ignore[index]
            verbose=True
        )

    @agent
    def blog_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['blog_writer'], # type: ignore[index]
            verbose=True
        )

    @agent
    def proofreader(self) -> Agent:
        return Agent(
            config=self.agents_config['proofreader'], # type: ignore[index]
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
            max_retries=2  # Research tasks can be retried up to 2 times
        )

    @task
    def write_blog_task(self) -> Task:
        return Task(
            config=self.tasks_config['write_blog_task'], # type: ignore[index]
            output_file='blog_post.md',
            context=[self.research_task()],
            max_retries=3  # Writing tasks can be retried up to 3 times (more complex)
        )

    @task
    def proofread_task(self) -> Task:
        return Task(
            config=self.tasks_config['proofread_task'], # type: ignore[index]
            output_file='final_blog_post.md',
            context=[self.write_blog_task()],
            max_retries=2  # Proofreading tasks can be retried up to 2 times
        )

    @crew
    def crew(self) -> Crew:
        """Creates the BlogWriter crew with sequential processing."""
        return Crew(
            agents=[
                self.researcher(),
                self.blog_writer(),
                self.proofreader()
            ],
            tasks=[
                self.research_task(),
                self.write_blog_task(),
                self.proofread_task()
            ],
            process=Process.sequential,
            verbose=True,
        )
