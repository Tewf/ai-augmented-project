"""The three tasks of the method comparison: the bare sentence, the function the judge looks for, the module name.

The sentences and the Decided lines are those of the brief test (ai-augmented-agents, round two), kept word for word,
so that the two experiments share their tasks. The hidden tests are in hidden/, one file per task.
"""
TASKS = {
    "scope": {
        "function": "scope_in_rows",
        "sentence": "Write a Python function that parses a Markdown scope table and lists its \"in\" rows, and tests for it.",
    },
    "changelog": {
        "function": "changelog_releases",
        "sentence": "Write a Python function that parses a Markdown changelog and lists its released versions with their dates, and tests for it.",
    },
    "llms": {
        "function": "llms_links",
        "sentence": "Write a Python function that parses the link list of an llms.txt file and returns each link with its description, and tests for it.",
    },
}
ARMS = ("alone", "method")
