# Day 1 – Comparing a Plain Chatbot, Rule-Based Workflow, and AI Agent

## 1. Scenario

For this task, I selected a personal study task management scenario. The purpose is to compare how a plain chatbot, a rule-based workflow, and an AI agent handle the same type of user request when private study information is involved.

The private data is stored in `data/study_data.json`. It contains study subjects, their priorities, deadlines, and completion status.

The sample private data contains four subjects: Data Structures, Python, Java, and Database Management. Data Structures and Database Management are marked as high priority, Java is completed, and the remaining subjects are pending.

The common type of request used in the demonstrations is asking what subjects should be studied or prioritized.

---

# 2. Plain Chatbot

## How it works

The plain chatbot uses the Groq LLM to generate responses to the user's messages. The application sends the user's request to the language model and displays the generated response.

The chatbot does not have any tools and does not provide the model with the contents of the private study data.

The flow is:

```text
User request
     ↓
Groq LLM
     ↓
Generated response