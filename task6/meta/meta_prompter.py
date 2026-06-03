from groq import Groq
import os

# -----------------------------
# CONFIG
# -----------------------------

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = "openai/gpt-oss-120b"

# -----------------------------
# LOAD META PROMPT
# -----------------------------

with open(
    "meta_prompt.txt",
    "r",
    encoding="utf-8"
) as f:

    META_PROMPT = f.read()

# -----------------------------
# GET USER BRIEF
# -----------------------------

brief = input(
    "Enter a vague brief: "
)

prompt = META_PROMPT.format(
    brief=brief
)

# -----------------------------
# GENERATE PROMPT
# -----------------------------

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

generated_prompt = (
    response.choices[0]
    .message
    .content
)

# -----------------------------
# DISPLAY RESULT
# -----------------------------

print("\n")
print("=" * 60)
print("GENERATED PROMPT")
print("=" * 60)
print()

print(generated_prompt)