# `chatutils`

`chatutils` is a Python library for text processing, rich display, and LLM helpers.

## Installation

```bash
pip install -U chatutils
```

## Example

```python
"""
Example script demonstrating `chatutils` in a realistic LLM workflow.
"""

import os
import chatutils
import openai

# We use Groq as an example LLM provider,
# as they provide their latest agent under the same name
model_name = "groq/compound"
client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY"),
)

# 2. The Payload: Construct role-based messages cleanly
messages = [
    chatutils.system("You are the state-of-the-art AI."),
    chatutils.user(
        """

        Write a minimal Python function to beep upon unexpected error,
        with an example usage in `if __name__ == "__main__"` clause.
        """
    ),  # This gets automatically formatted internally
]

# Display **exactly** what we are sending to the LLM.
# You see the indented prompt is properly formatted
chatutils.print_chat_messages(messages)

# Fire the request (assuming success because we are optimists)
response = client.chat.completions.create(model=model_name, messages=messages)
content = chatutils.get_completion(response)  # obtain response.choices[0].message.content

chatutils.print_panel(content, title="Response", border_style="green")

# Save the context & completion
messages.append(chatutils.assistant(content))
cache_filepath = (
    ".llm_cache/messages--"
    f"{model_name.replace('/', '_')}.{chatutils.hash_messages(messages)}"
    ".jsonl"
)
chatutils.save_messages(messages, cache_filepath)

code = chatutils.parse(content, index=-1)  # Parse the last code block
chatutils.write(code, "beep.py")
```

The same code is available in [./example.py](https://github.com/kyo-takano/chatutils/blob/main/example.py):
