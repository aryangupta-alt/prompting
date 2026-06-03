from google import genai
import os

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL = "gemini-3.5-flash"

email = """
My account was hacked and unauthorized purchases were made.
"""

prompts = {

    "FULL PROMPT": f"""
Role:
You are a customer support email triage specialist.

Context:
Customer support teams receive a large number of emails every day. Emails must be categorized so that urgent issues are handled first.

Task:
Classify each email into one of the following categories:

- Urgent
- Normal
- Spam

Constraints:
- Choose only one category.
- Do not provide explanations.
- Return only the category name.

Format:
Single-word classification.

Examples:

Input:
My account was hacked and unauthorized purchases were made.

Output:
Urgent

Input:
Can you tell me when my order will arrive?

Output:
Normal

Input:
Congratulations! You have won a free iPhone. Click here now!

Output:
Spam

Email:
{email}
""",

    "WITHOUT ROLE": f"""
Context:
Customer support teams receive a large number of emails every day. Emails must be categorized so that urgent issues are handled first.

Task:
Classify each email into one of the following categories:

- Urgent
- Normal
- Spam

Constraints:
- Choose only one category.
- Do not provide explanations.
- Return only the category name.

Format:
Single-word classification.

Examples:

Input:
My account was hacked and unauthorized purchases were made.

Output:
Urgent

Input:
Can you tell me when my order will arrive?

Output:
Normal

Input:
Congratulations! You have won a free iPhone. Click here now!

Output:
Spam

Email:
{email}
""",

    "WITHOUT CONTEXT": f"""
Role:
You are a customer support email triage specialist.

Task:
Classify each email into one of the following categories:

- Urgent
- Normal
- Spam

Constraints:
- Choose only one category.
- Do not provide explanations.
- Return only the category name.

Format:
Single-word classification.

Examples:

Input:
My account was hacked and unauthorized purchases were made.

Output:
Urgent

Input:
Can you tell me when my order will arrive?

Output:
Normal

Input:
Congratulations! You have won a free iPhone. Click here now!

Output:
Spam

Email:
{email}
""",

    "WITHOUT CONSTRAINTS": f"""
Role:
You are a customer support email triage specialist.

Context:
Customer support teams receive a large number of emails every day. Emails must be categorized so that urgent issues are handled first.

Task:
Classify each email into one of the following categories:

- Urgent
- Normal
- Spam

Format:
Single-word classification.

Examples:

Input:
My account was hacked and unauthorized purchases were made.

Output:
Urgent

Input:
Can you tell me when my order will arrive?

Output:
Normal

Input:
Congratulations! You have won a free iPhone. Click here now!

Output:
Spam

Email:
{email}
""",

    "WITHOUT FORMAT": f"""
Role:
You are a customer support email triage specialist.

Context:
Customer support teams receive a large number of emails every day. Emails must be categorized so that urgent issues are handled first.

Task:
Classify each email into one of the following categories:

- Urgent
- Normal
- Spam

Constraints:
- Choose only one category.
- Do not provide explanations.
- Return only the category name.

Examples:

Input:
My account was hacked and unauthorized purchases were made.

Output:
Urgent

Input:
Can you tell me when my order will arrive?

Output:
Normal

Input:
Congratulations! You have won a free iPhone. Click here now!

Output:
Spam

Email:
{email}
""",

    "WITHOUT EXAMPLES": f"""
Role:
You are a customer support email triage specialist.

Context:
Customer support teams receive a large number of emails every day. Emails must be categorized so that urgent issues are handled first.

Task:
Classify each email into one of the following categories:

- Urgent
- Normal
- Spam

Constraints:
- Choose only one category.
- Do not provide explanations.
- Return only the category name.

Format:
Single-word classification.

Email:
{email}
"""
}

for title, prompt in prompts.items():

    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    print(response.text)