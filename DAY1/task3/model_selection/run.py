from groq import Groq  # type: ignore[reportMissingImports]
import os
import time
import csv

# Initialize Groq Client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Models to Compare
MODELS = [
    "openai/gpt-oss-120b",
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "allam-2-7b"
]

# Pricing ($ per 1M tokens)
PRICING = {
    "openai/gpt-oss-120b": {
        "input": 0.15,
        "output": 0.60
    },
    "meta-llama/llama-4-scout-17b-16e-instruct": {
        "input": 0.11,
        "output": 0.34
    },
    "allam-2-7b": {
        "input": 0.00,
        "output": 0.00
    }
}

def judge_summary(document, summary):

    judge_prompt = f"""
You are evaluating a document summary.

Original Document:
{document}

Summary:
{summary}

Rate the summary on:

1. Accuracy
2. Completeness
3. Clarity

Scoring:
5 = Excellent
4 = Good
3 = Average
2 = Poor
1 = Very Poor

Return ONLY one character:
1
2
3
4
or
5

Do not provide explanations.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": judge_prompt
            }
        ]
    )

    score = (
        response.choices[0]
        .message
        .content
        .strip()
    )

    try:
        return int(score)
    except:
        return ""

# Prompt Template
PROMPT_TEMPLATE = """
Summarize the following document into exactly 3 bullet points.

Document:
{document}
"""

# Create Results CSV
with open(
    "results.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "input_id",
        "model",
        "latency_ms",
        "input_tokens",
        "output_tokens",
        "cost_usd",
        "quality_score_1to5",
        "notes"
    ])

    # Loop through all documents
    for i in range(1, 21):

        try:

            with open(
                f"inputs/doc{i}.txt",
                "r",
                encoding="utf-8"
            ) as f:

                document = f.read()

        except Exception as e:

            print(f"Could not read doc{i}.txt")
            continue

        prompt = PROMPT_TEMPLATE.format(
            document=document
        )

        # Run each model
        for model in MODELS:

            try:

                print(f"Running Doc {i} | {model}")

                start_time = time.time()

                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                latency_ms = round(
                    (time.time() - start_time) * 1000
                )

                summary = (
                    response.choices[0]
                    .message
                    .content
                )

                # Token Usage
                input_tokens = (
                    response.usage.prompt_tokens
                    if response.usage
                    else 0
                )

                output_tokens = (
                    response.usage.completion_tokens
                    if response.usage
                    else 0
                )

                # Cost Calculation
                cost_usd = (
                    (input_tokens / 1_000_000)
                    * PRICING[model]["input"]
                ) + (
                    (output_tokens / 1_000_000)
                    * PRICING[model]["output"]
                )

                quality_score = judge_summary(
                    document,
                    summary
                )

                # Create Outputs Folder
                os.makedirs(
                    "outputs",
                    exist_ok=True
                )

                safe_model_name = model.replace("/", "_")

                output_file = (
                    f"outputs/doc{i}_"
                    f"{safe_model_name}.txt"
                )

                with open(
                    output_file,
                    "w",
                    encoding="utf-8"
                ) as out:

                    out.write(summary)

                writer.writerow([
    i,
    model,
    latency_ms,
    input_tokens,
    output_tokens,
    round(cost_usd, 8),
    quality_score,
    "Success"
])

                print(
                    f"Completed Doc {i} | {model}"
                )

            except Exception as e:

                print(
                    f"Failed Doc {i} | {model}"
                )

                writer.writerow([
                    i,
                    model,
                    "",
                    "",
                    "",
                    "",
                    "",
                    str(e)
                ])

print("\nFinished.")
print("Results saved to results.csv")