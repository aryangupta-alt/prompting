from google import genai
import os

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL = "gemini-3.5-flash"

claim = """
The policyholder reported that their parked vehicle was struck by another car in a shopping mall parking lot. The rear bumper and left tail light were damaged. No injuries were reported. A police report was filed.
"""

prompts = {
    "FULL PROMPT": f"""
Role:
You are an experienced insurance claims analyst.

Context:
Insurance claim reports are often long and contain unnecessary details.

Task:
Summarize the insurance claim.

Constraints:
- Keep under 100 words
- Include only key facts

Format:
Bullet points

Examples:
Input: Vehicle accident
Output: • Accident occurred

Claim:
{claim}
""",

    "WITHOUT ROLE": f"""
Context:
Insurance claim reports are often long and contain unnecessary details.

Task:
Summarize the insurance claim.

Constraints:
- Keep under 100 words

Format:
Bullet points

Claim:
{claim}
""",

    "WITHOUT CONTEXT": f"""
Role:
You are an experienced insurance claims analyst.

Task:
Summarize the insurance claim.

Constraints:
- Keep under 100 words

Format:
Bullet points

Claim:
{claim}
""",

    "WITHOUT CONSTRAINTS": f"""
Role:
You are an experienced insurance claims analyst.

Context:
Insurance claim reports are often long and contain unnecessary details.

Task:
Summarize the insurance claim.

Format:
Bullet points

Claim:
{claim}
""",

    "WITHOUT FORMAT": f"""
Role:
You are an experienced insurance claims analyst.

Context:
Insurance claim reports are often long and contain unnecessary details.

Task:
Summarize the insurance claim.

Constraints:
- Keep under 100 words

Claim:
{claim}
""",

    "WITHOUT EXAMPLES": f"""
Role:
You are an experienced insurance claims analyst.

Context:
Insurance claim reports are often long and contain unnecessary details.

Task:
Summarize the insurance claim.

Constraints:
- Keep under 100 words

Format:
Bullet points

Claim:
{claim}
"""
}

for title, prompt in prompts.items():

    print("\n" + "="*60)
    print(title)
    print("="*60)

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    print(response.text)