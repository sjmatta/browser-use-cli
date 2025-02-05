from langchain_openai import ChatOpenAI
import logging

logger = logging.getLogger(__name__)

class BrowserAgent:
    def __init__(self, console, max_actions):
        self.__console = console
        self.__max_actions = max_actions

    async def run(self, input_text, max_actions=None):
        """
        Runs the agent with the provided arguments.
        Args:
            arguments (str): The task arguments for the agent.
        Returns:
            result: The result of the agent's execution.
        """
        agent_args = {
            "task": input_text,
            "llm": ChatOpenAI(model="gpt-4o"),
            "generate_gif": False,
        }
        if self.__max_actions is not None:
            agent_args["max_actions_per_step"] = __max_actions

        # disabling pylint here because browser_use does too much with the logging config
        # if we import it before our own logging configuration
        # pylint: disable-next=import-outside-toplevel
        from browser_use import Agent

        agent = Agent(**agent_args)
        status = self.__console.status("[bold green]Automating your browser to answer your query...", spinner="earth")

        status.start()
        result = await agent.run()
        status.stop()

        for error in result.errors():
            logger.error(error)

        return result