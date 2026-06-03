import warnings
warnings.filterwarnings("ignore")

from google import genai
import os

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL = "gemini-3.5-flash"

product = """
Wireless Bluetooth Headphones with Noise Cancellation and 30-hour battery life.
"""

prompts = {

    "FULL PROMPT": f"""
Role:
You are a professional marketing copywriter.

Context:
E-commerce businesses often need product descriptions rewritten to make them more appealing and customer-friendly.

Task:
Rewrite the product description in a friendly and engaging tone.

Constraints:
- Do not change product features.
- Do not add new features.
- Keep the description concise.
- Maintain factual accuracy.

Format:
Return a single paragraph.

Examples:

Input:
Durable stainless steel water bottle.

Output:
Stay hydrated throughout the day with this durable stainless steel water bottle, designed to keep up with your active lifestyle.

Product:
{product}
""",

    "WITHOUT ROLE": f"""
Context:
E-commerce businesses often need product descriptions rewritten to make them more appealing and customer-friendly.

Task:
Rewrite the product description in a friendly and engaging tone.

Constraints:
- Do not change product features.
- Do not add new features.
- Keep the description concise.
- Maintain factual accuracy.

Format:
Return a single paragraph.

Examples:

Input:
Durable stainless steel water bottle.

Output:
Stay hydrated throughout the day with this durable stainless steel water bottle, designed to keep up with your active lifestyle.

Product:
{product}
""",

    "WITHOUT CONTEXT": f"""
Role:
You are a professional marketing copywriter.

Task:
Rewrite the product description in a friendly and engaging tone.

Constraints:
- Do not change product features.
- Do not add new features.
- Keep the description concise.
- Maintain factual accuracy.

Format:
Return a single paragraph.

Examples:

Input:
Durable stainless steel water bottle.

Output:
Stay hydrated throughout the day with this durable stainless steel water bottle, designed to keep up with your active lifestyle.

Product:
{product}
""",

    "WITHOUT CONSTRAINTS": f"""
Role:
You are a professional marketing copywriter.

Context:
E-commerce businesses often need product descriptions rewritten to make them more appealing and customer-friendly.

Task:
Rewrite the product description in a friendly and engaging tone.

Format:
Return a single paragraph.

Examples:

Input:
Durable stainless steel water bottle.

Output:
Stay hydrated throughout the day with this durable stainless steel water bottle, designed to keep up with your active lifestyle.

Product:
{product}
""",

    "WITHOUT FORMAT": f"""
Role:
You are a professional marketing copywriter.

Context:
E-commerce businesses often need product descriptions rewritten to make them more appealing and customer-friendly.

Task:
Rewrite the product description in a friendly and engaging tone.

Constraints:
- Do not change product features.
- Do not add new features.
- Keep the description concise.
- Maintain factual accuracy.

Examples:

Input:
Durable stainless steel water bottle.

Output:
Stay hydrated throughout the day with this durable stainless steel water bottle, designed to keep up with your active lifestyle.

Product:
{product}
""",

    "WITHOUT EXAMPLES": f"""
Role:
You are a professional marketing copywriter.

Context:
E-commerce businesses often need product descriptions rewritten to make them more appealing and customer-friendly.

Task:
Rewrite the product description in a friendly and engaging tone.

Constraints:
- Do not change product features.
- Do not add new features.
- Keep the description concise.
- Maintain factual accuracy.

Format:
Return a single paragraph.

Product:
{product}
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