import json

# Read private study data
with open("data/study_data.json", "r") as file:
    data = json.load(file)

subjects = data["subjects"]

print("================================")
print("      RULE-BASED WORKFLOW")
print("================================")

user_input = input("\nYou: ")

print("\nWorkflow processing...")

# Find incomplete subjects
pending_tasks = [
    subject
    for subject in subjects
    if subject["completed"] is False
]

# Find high-priority pending subjects
high_priority_tasks = [
    subject
    for subject in pending_tasks
    if subject["priority"] == "High"
]

# Predefined rules
if "study" in user_input.lower() or "today" in user_input.lower():

    print("\nWorkflow:")
    print("You should focus on:")

    for subject in high_priority_tasks:
        print(
            f"- {subject['name']} "
            f"(deadline: {subject['deadline']})"
        )

elif "pending" in user_input.lower():

    print("\nWorkflow:")
    print("Your pending subjects are:")

    for subject in pending_tasks:
        print(f"- {subject['name']}")

else:

    print("\nWorkflow:")
    print("Sorry, this workflow only understands predefined requests.")