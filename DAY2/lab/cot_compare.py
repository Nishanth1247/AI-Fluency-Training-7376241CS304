from config import client, MODEL


QUESTIONS = [
    "A course costs Rs. 12,000. Apply a 15% scholarship, then split the final amount into 4 equal installments. What is each installment?",

    "A lab has 18 computers. If 2 students use each computer in the morning and 3 students use each computer in the afternoon, how many student sittings are possible in one day?",

    "Ravi is taller than Kumar. Kumar is taller than Arun. Priya is shorter than Arun. Who is the tallest and who is the shortest?"
]


DIRECT_PROMPT = (
    "You are a helpful assistant. "
    "Give only the final answer. Do not explain."
)


COT_PROMPT = (
    "You are a helpful assistant. "
    "Solve the problem step by step. "
    "Number each step and show the calculation in that step. "
    "After the steps, write the last line exactly as: "
    "Final Answer: <answer>"
)


def ask(question, system_prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()


for i, question in enumerate(QUESTIONS, start=1):

    direct = ask(question, DIRECT_PROMPT)
    cot = ask(question, COT_PROMPT)

    print("\n" + "=" * 70)
    print(f"QUESTION {i}")
    print(question)

    print("\n--- WITHOUT CoT ---")
    print(direct)

    print("\n--- WITH CoT ---")
    print(cot)

    print("\nLENGTH")
    print("Without CoT:", len(direct), "characters")
    print("With CoT   :", len(cot), "characters")