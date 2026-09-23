
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = os.getenv("MODEL", "openai/gpt-oss-120b")


QUESTIONS = [
    "Which is cheaper: CS101 and AI202 with a 10% scholarship, or all three courses with a 25% scholarship? By how much?",

    "A course costs Rs. 12,000. Apply a 15% scholarship, then split the final amount into 4 equal installments. What is each installment?",

    "A lab has 18 computers. If 2 students use each computer in the morning and 3 students use each computer in the afternoon, how many student sittings are possible in one day?",

    "Ravi is taller than Kumar. Kumar is taller than Arun. Priya is shorter than Arun. Who is the tallest and who is the shortest?"
]


SYSTEM_PROMPT = (
    "You are a helpful college assistant. "
    "Answer directly using only your existing knowledge. "
    "Do not use tools. "
    "Do not show your reasoning."
)


for i, question in enumerate(QUESTIONS, start=1):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0
    )

    answer = response.choices[0].message.content.strip()

    print("\n" + "=" * 70)
    print(f"QUESTION {i}")
    print(question)

    print("\nDIRECT ANSWER:")
    print(answer)
