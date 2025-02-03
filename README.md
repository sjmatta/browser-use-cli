Just a quick use of https://github.com/browser-use/browser-use. Not sure where I'll go with it. Currently, I'm finding it useful for finding information on more niche websites.

Any ideas? Open an issue.

## Setup
Note: I use pyenv, so I set up pyenv with `pyenv virtualenv 3.13 browser-use` which is why `.python-version` has `browser-use` in it. If you have a better suggestion for my workflow, please open an issue and suggest it!
1. Ensure you have OPENAI_API_KEY defined in your environment, or your .env file
1. `pip install -r requirements.txt`
1. `playwright install`
1. `python src/main.py`

You can also pipe instructions as input: `echo "Summarize today's news from The 51st (at https://51st.news/)" | python src/main.py`

TODO:
1. Allow choosing from different LLMs
1. Better output of results
1. Pipeline finishers- summarization, providing a report, synthesizing information, etc.
1. Find many examples of niche use cases where this works better than Perplexity or ChatGPT search (usually, those work better and are significantly less expensive per query)
1. Why does it create an image file
1. Allow choosing a clean browser, or using an existing Chrome instance, with existing cookies, for automating some tasks