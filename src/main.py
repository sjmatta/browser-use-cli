"""A CLI application for browser automation using https://github.com/browser-use/browser-use"""
import argparse
import asyncio
import logging
import readline # type: ignore pylint: disable=unused-import | used by rich
import select
import sys

from dotenv import load_dotenv
from rich.console import Console
from rich.logging import RichHandler
from rich.markdown import Markdown

from agent import BrowserAgent

logger = logging.getLogger(__name__)
console = Console()

def parse_arguments():
    """
    Parses command-line arguments.
    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="A CLI tool with logging.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument(
        "-m",
        "--max-actions",
        type=int,
        default=None,
        help="Maximum actions per step (max_actions_per_step in browser-use)",
    )
    return parser.parse_args()


def get_input():
    """
    Reads input from either a pipe or user prompt.
    This function checks if there is data available in the standard input pipe.
    If data is available in the pipe, it reads and returns that data.
    Otherwise, it prompts the user for input directly.
    Returns:
        str: The input string from either pipe or user prompt, with leading/trailing
             whitespace removed
    """

    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        return sys.stdin.read().strip()  # Read from pipe
    return console.input("Enter input: ").strip()


def configure_logging(verbose):
    """
    Configures logging based on verbosity.
    Args:
        verbose (bool): Flag to enable verbose logging.
    """
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[RichHandler(rich_tracebacks=True)],
    )

    browser_use_logger = logging.getLogger("browser_use")
    browser_use_logger.setLevel(logging.INFO if verbose else logging.WARN)

    # Silence third-party loggers
    # See https://github.com/browser-use/browser-use/blob/4ebcb43a983b37a5fa551ac3d70258f4e8a61ea9/browser_use/logging_config.py#L113
    for third_party_logger in [
        "WDM",
        "httpx",
        "selenium",
        "playwright",
        "urllib3",
        "asyncio",
        "langchain",
        "openai",
        "httpcore",
        "charset_normalizer",
        "anthropic._base_client",
        "PIL.PngImagePlugin",
        "trafilatura.htmlprocessing",
        "trafilatura",
    ]:
        third_party = logging.getLogger(third_party_logger)
        third_party.setLevel(logging.ERROR)
        third_party.propagate = False

async def main():
    """
    Main function that processes arguments and runs the agent.
    """
    load_dotenv()
    args = parse_arguments()
    configure_logging(args.verbose)

    input_text = get_input()

    browser_agent = BrowserAgent(console, args.max_actions)
    result = await browser_agent.run(input_text)
    console.print(Markdown(result.final_result()))


if __name__ == "__main__":
    asyncio.run(main())

    # the next line seems to be needed to prevent an asyncio error
    console.__exit__(None, None, None)
