
import os
import re
from collections import Counter

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = os.getenv("MODEL", "openai/gpt-oss-120b")

QUESTION = (
    "A course costs Rs. 12,000. Apply a 15% scholarship, "
    "then split the final amount into 4 equal installments. "
    "What is each installment?"
)

RUNS = 5
TEMPERATURE = 0.8

PROMPT = (
    "You are a helpful assistant. "
    "Solve the problem step by step. "
    "Number each step and show the calculation in that step. "
    "After the steps, write the last line exactly as: "
    "Final Answer: <answer>"
)


def ask():
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": QUESTION}
        ],
        temperature=TEMPERATURE
    )

    return response.choices[0].message.content.strip()


def extract_final_answer(response):
    match = re.search(
        r"Final Answer:\s*(.+)",
        response,
        re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    return response.strip()


def normalize_answer(answer):
    numbers = re.findall(
        r"\d+(?:,\d+)*(?:\.\d+)?",
        answer
    )

    if numbers:
        return numbers[-1].replace(",", "")

    return answer.lower().strip()


answers = []

for run in range(1, RUNS + 1):

    response = ask()
    final_answer = extract_final_answer(response)
    normalized = normalize_answer(final_answer)

    print("\n" + "=" * 70)
    print(f"RUN {run}")
    print(response)
    print(f"\nExtracted answer: {final_answer}")
    print(f"Normalized answer: {normalized}")

    answers.append(normalized)


counts = Counter(answers)

print("\n" + "=" * 70)
print("SELF-CONSISTENCY SUMMARY")

for answer, count in counts.items():
    print(f"{answer} -> {count}/{RUNS}")

majority_answer, majority_count = counts.most_common(1)[0]

print("\nMAJORITY ANSWER")
print(f"{majority_answer} -> {majority_count}/{RUNS}")

if majority_answer == "2550":
    print("Result: CORRECT")
else:
    print("Result: INCORRECT")
