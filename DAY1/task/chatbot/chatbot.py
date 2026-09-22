import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

print("================================")
print("       PLAIN STUDY CHATBOT")
print("================================")
print("Type 'exit' to stop.\n")

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Chatbot: Goodbye!")
        break

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": """
You are a general study assistant.
You can answer questions and provide general
study advice.

You do NOT have access to the student's
private study data.
"""
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    answer = response.choices[0].message.content

    print("\nChatbot:", answer)
    print()