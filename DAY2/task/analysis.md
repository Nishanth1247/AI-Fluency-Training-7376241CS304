# Day 2 Task: Reasoning and Acting

## Scenario: College Course Fee Assistant

### 1. Scenario Description

For this task, I selected a college course fee assistant scenario. The system has access to the following private course-fee information:

| Course | Fee |
|---|---:|
| CS101 | Rs. 12,000 |
| AI202 | Rs. 18,000 |
| DS303 | Rs. 15,000 |

The main multi-step question used to compare the three approaches was:

> Which is cheaper: CS101 and AI202 with a 10% scholarship, or all three courses with a 25% scholarship? By how much?

The correct calculation is:

- CS101 + AI202 = Rs. 12,000 + Rs. 18,000 = Rs. 30,000
- After a 10% scholarship = Rs. 27,000
- All three courses = Rs. 12,000 + Rs. 18,000 + Rs. 15,000 = Rs. 45,000
- After a 25% scholarship = Rs. 33,750
- Difference = Rs. 33,750 - Rs. 27,000 = Rs. 6,750

Therefore, the first option is cheaper by Rs. 6,750.

Three additional reasoning questions were used:

1. A course costs Rs. 12,000. Apply a 15% scholarship, then split the final amount into 4 equal installments.
2. A lab has 18 computers. If 2 students use each computer in the morning and 3 students use each computer in the afternoon, how many student sittings are possible in one day?
3. Ravi is taller than Kumar. Kumar is taller than Arun. Priya is shorter than Arun. Who is the tallest and who is the shortest?

These questions allowed the approaches to be compared on both tool-dependent and reasoning-only problems.

---

# 2. Direct Prompting

Direct prompting asks the language model to answer the user's question immediately. It does not provide tools and does not give the model access to the private course-fee data.

In this experiment, the model was instructed to answer directly using its existing knowledge and not to use tools or show its reasoning.

For the main course comparison question, direct prompting could not produce the correct numerical answer because the course prices were not included in the question itself and the model had no access to the private course-fee data. Instead, it represented the course fees as variables and explained how the comparison could be calculated if the prices were provided.

This demonstrates an important limitation of direct prompting: reasoning alone cannot provide private or external information that is not available in the prompt or the model's existing knowledge.

For the three reasoning questions, direct prompting performed correctly because all the required information was already included in each question. It calculated the installment as Rs. 2,550, calculated 90 student sittings, and identified Ravi as the tallest and Priya as the shortest.

Direct prompting is therefore simple and fast when the question contains all the required information. Its main limitation in this scenario was its inability to retrieve the private course-fee information.

---

# 3. Chain-of-Thought Prompting

Chain-of-Thought prompting asks the model to solve a problem step by step before producing the final answer. In this experiment, the model was instructed to number the steps, show the calculations or reasoning, and then provide a final answer.

For the main course comparison question, Chain-of-Thought identified the information that was missing. It recognized that the prices of CS101, AI202, and the third course were required and wrote formulas for comparing the two options. However, it could not retrieve the actual private fees. It therefore stopped and requested the course prices instead of producing the correct numerical result.

This shows that Chain-of-Thought can make the reasoning process more explicit and can help with multi-step calculations, but it does not give the model access to information that it does not have.

For the other three questions, Chain-of-Thought produced correct answers. It calculated Rs. 2,550 for the installment question, 90 for the lab sittings question, and identified Ravi as the tallest and Priya as the shortest.

The Chain-of-Thought responses were also much longer than the direct responses because they included intermediate calculations and reasoning steps. For example, the installment question was solved by first calculating the Rs. 1,800 scholarship, then calculating the Rs. 10,200 payable amount, and finally dividing it into four installments.

Therefore, Chain-of-Thought is useful when a problem requires several reasoning steps, but it does not replace tools when external or private information is required.

---

# 4. ReAct Agent

ReAct combines reasoning and acting. Instead of only producing an answer, the agent can determine what information it needs, call an appropriate tool, observe the result, and continue until it has enough information to answer.

For this task, the ReAct agent had two tools:

- `get_course_fee` — retrieves the fee of CS101, AI202, or DS303.
- `calculator` — performs arithmetic calculations.

The agent was instructed never to guess private course fees and to use the calculator for arithmetic.

For the main course comparison question, the agent first called the course-fee tool for CS101, AI202, and DS303. It received Rs. 12,000, Rs. 18,000, and Rs. 15,000 respectively.

It then used the calculator to calculate:

```text
(12000 + 18000) * 0.9 = 27000