from groq import Groq
import os

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = "openai/gpt-oss-120b"

with open(
    "meta_prompt.txt",
    "r",
    encoding="utf-8"
) as f:
    META_PROMPT = f.read()

briefs = [
    "extract data from PDFs",
    "classify support emails",
    "write product descriptions",
    "summarize legal documents",
    "translate marketing copy"
]

os.makedirs(
    "generated_prompts",
    exist_ok=True
)

for i, brief in enumerate(briefs, start=1):

    print(f"Generating Prompt {i}")

    prompt = META_PROMPT.format(
        brief=brief
    )

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

    with open(
        f"generated_prompts/brief{i}.txt",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(generated_prompt)

print("\nAll prompts generated.")