
import os
import json
import ast
import operator as op

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = os.getenv("MODEL", "openai/gpt-oss-120b")


COURSE_FEES = {
    "CS101": 12000,
    "AI202": 18000,
    "DS303": 15000
}


def get_course_fee(course_code):
    course_code = course_code.upper()

    if course_code not in COURSE_FEES:
        return f"Unknown course: {course_code}"

    return COURSE_FEES[course_code]


OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.USub: op.neg
}


def calculator(expression):

    def evaluate(node):

        if isinstance(node, ast.Constant):
            return node.value

        if isinstance(node, ast.BinOp):
            left = evaluate(node.left)
            right = evaluate(node.right)
            operation = OPERATORS[type(node.op)]
            return operation(left, right)

        if isinstance(node, ast.UnaryOp):
            operand = evaluate(node.operand)
            operation = OPERATORS[type(node.op)]
            return operation(operand)

        raise ValueError("Unsupported expression")

    tree = ast.parse(expression, mode="eval")

    return evaluate(tree.body)


TOOL_FUNCTIONS = {
    "get_course_fee": get_course_fee,
    "calculator": calculator
}


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_course_fee",
            "description": "Get the fee for a course.",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_code": {
                        "type": "string",
                        "description": "Course code such as CS101, AI202, or DS303"
                    }
                },
                "required": ["course_code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to calculate"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]


QUESTIONS = [
    "Which is cheaper: CS101 and AI202 with a 10% scholarship, or all three courses with a 25% scholarship? By how much?",

    "A course costs Rs. 12,000. Apply a 15% scholarship, then split the final amount into 4 equal installments. What is each installment?",

    "A lab has 18 computers. If 2 students use each computer in the morning and 3 students use each computer in the afternoon, how many student sittings are possible in one day?",

    "Ravi is taller than Kumar. Kumar is taller than Arun. Priya is shorter than Arun. Who is the tallest and who is the shortest?"
]


SYSTEM_PROMPT = (
    "You are a college assistant. "
    "Use get_course_fee whenever course fee information is needed. "
    "Never guess private course fees. "
    "Use calculator for arithmetic. "
    "If no tool is needed, answer directly."
)


def run_agent(question, max_steps=8):

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

        if not message.tool_calls:
            return message.content.strip()

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

        for call in message.tool_calls:

            name = call.function.name
            arguments = json.loads(call.function.arguments or "{}")

            function = TOOL_FUNCTIONS[name]
            result = function(**arguments)

            print(
                f"Step {step} | "
                f"Action: {name}({arguments}) | "
                f"Observation: {result}"
            )

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": str(result)
            })

    return "Maximum steps reached."


for i, question in enumerate(QUESTIONS, start=1):

    print("\n" + "=" * 70)
    print(f"QUESTION {i}")
    print(question)

    answer = run_agent(question)

    print("\nREACT FINAL ANSWER:")
    print(answer)
