import os

from dotenv import load_dotenv
from groq import Groq

from tools import available_tools


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = "openai/gpt-oss-120b"


# Tools given to the LLM
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_pending_tasks",
            "description": "Get all study subjects that have not been completed.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_all_tasks",
            "description": "Get all study subjects including completed and incomplete subjects.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_high_priority_tasks",
            "description": "Get incomplete subjects that have High priority.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]


def run_agent(user_input):

    messages = [
        {
            "role": "system",
            "content": """
You are a personal study assistant.

The student has private study information.

You do not have direct access to the private data.

When the user's question requires private study information,
use the appropriate tool.

After receiving the tool result, analyze the information
and provide a clear answer.

Do not claim to know private information unless you
obtained it through a tool.
"""
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    # AGENT LOOP
    while True:

        print("\n[Agent] Calling LLM...")

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        # If the LLM does not request a tool,
        # the agent has reached its final answer.
        if not message.tool_calls:

            return message.content

        # Add the assistant's tool request
        messages.append(message)

        # Execute every requested tool
        for tool_call in message.tool_calls:

            function_name = tool_call.function.name

            print(f"[Agent] Selected tool: {function_name}")

            function = available_tools.get(function_name)

            if function is None:

                result = "Error: tool not found."

            else:

                result = function()

            print("[Agent] Tool executed.")

            # Give the tool result back to the LLM
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                }
            )


print("================================")
print("          AI AGENT")
print("================================")
print("Type 'exit' to stop.\n")


while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":

        print("Agent: Goodbye!")
        break

    answer = run_agent(user_input)

    print("\nAgent:")
    print(answer)
    print()
    