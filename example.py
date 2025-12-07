#!/usr/bin/env python3
"""
Example script demonstrating `chatutils` in a realistic LLM workflow.
"""

import os
import openai
import chatutils

"""
We use Groq as an example LLM provider,
as they provide their latest agent under the same name
"""
model_name = "groq/compound"
client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY"),
)

"""
Construct the messages for the chat model to complete
"""
messages = [
    chatutils.system("You are the state-of-the-art AI."),
    chatutils.user(
        """

        Write a minimal Python function to beep upon unexpected error,
        with an example usage in `if __name__ == "__main__"` clause.
        """
    ),  # This gets automatically formatted internally
]

"""
Display **exactly** what we are sending to the LLM.
"""
chatutils.print_chat_messages(messages)
# You see the indented prompt is properly formatted

"""
Fire the request
"""
response = client.chat.completions.create(
    model=model_name,
    messages=messages,
)
# obtain response.choices[0].message.content
content = chatutils.get_content(response)

chatutils.print_panel(content, title="Response", border_style="green")

"""
Save the context & completion
"""
messages.append(chatutils.assistant(content))
chatutils.save_messages(
    messages,
    (
        ".llm_cache/messages--"
        f"{model_name.replace('/', '_')}.{chatutils.hash_messages(messages)}"
        ".jsonl"
    ),
)

code = chatutils.parse(content, index=-1)  # Parse the last code block
chatutils.write(code, "beep.py")


os.system("python beep.py")  # should be executable!
