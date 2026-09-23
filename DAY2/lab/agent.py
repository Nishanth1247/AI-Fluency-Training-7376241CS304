import json

from config import client, MODEL
from tools import TOOLS, TOOL_FUNCTIONS


SYSTEM_PROMPT = (
    "You are a college fee assistant. "
    "Never guess a fee: always use get_course_fee. "
    "Use calculator for any arithmetic. "
    "Available course codes: CS101, AI202, DS303. "
    "If no tool is needed, answer directly."
)


def agent(question, max_steps=8, verbose=True):
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": question
        }
    ]

    for step in range(1, max_steps + 1):

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            temperature=0
        )

        message = response.choices[0].message

        # No more tools needed → final answer
        if not message.tool_calls:
            return message.content.strip()

        # Add assistant tool-call message
        messages.append({
            "role": "assistant",
            "content": message.content or "",
            "tool_calls": [
                {
                    "id": call.id,
                    "type": "function",
                    "function": {
                        "name": call.function.name,
                        "arguments": call.function.arguments
                    }
                }
                for call in message.tool_calls
            ]
        })

        # Execute each tool
        for call in message.tool_calls:

            name = call.function.name
            arguments = json.loads(call.function.arguments or "{}")

            function = TOOL_FUNCTIONS.get(name)

            if function:
                result = function(**arguments)
            else:
                result = f"Unknown tool: {name}"

            if verbose:
                print(
                    f"   step {step}: "
                    f"{name}({arguments}) -> {result}"
                )

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": str(result)
            })

    return "Stopped: maximum steps reached without a final answer."