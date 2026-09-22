import json


def get_pending_tasks():
    """Return all incomplete study tasks."""

    with open("data/study_data.json", "r") as file:
        data = json.load(file)

    pending = [
        subject
        for subject in data["subjects"]
        if subject["completed"] is False
    ]

    return json.dumps(pending)


def get_all_tasks():
    """Return all study tasks."""

    with open("data/study_data.json", "r") as file:
        data = json.load(file)

    return json.dumps(data["subjects"])


def get_high_priority_tasks():
    """Return incomplete high-priority study tasks."""

    with open("data/study_data.json", "r") as file:
        data = json.load(file)

    high_priority = [
        subject
        for subject in data["subjects"]
        if subject["completed"] is False
        and subject["priority"] == "High"
    ]

    return json.dumps(high_priority)


available_tools = {
    "get_pending_tasks": get_pending_tasks,
    "get_all_tasks": get_all_tasks,
    "get_high_priority_tasks": get_high_priority_tasks
}