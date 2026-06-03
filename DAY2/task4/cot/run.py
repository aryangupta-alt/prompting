from groq import Groq
import os
import json
import csv
from collections import Counter

# -----------------------------
# CONFIG
# -----------------------------

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = "openai/gpt-oss-120b"

# GPT-OSS Pricing
INPUT_PRICE = 0.15
OUTPUT_PRICE = 0.60

# -----------------------------
# LOAD PROMPTS
# -----------------------------

with open("prompts/direct.txt", "r") as f:
    DIRECT_PROMPT = f.read()

with open("prompts/cot.txt", "r") as f:
    COT_PROMPT = f.read()

with open("prompts/sc.txt", "r") as f:
    SC_PROMPT = f.read()

# -----------------------------
# COST CALCULATION
# -----------------------------

def calculate_cost(input_tokens, output_tokens):

    return round(
        (
            input_tokens * INPUT_PRICE
            +
            output_tokens * OUTPUT_PRICE
        ) / 1_000_000,
        8
    )

# -----------------------------
# EXTRACT YES / NO
# -----------------------------

def extract_answer(text):

    text = text.strip().lower()

    if "yes" in text:
        return "Yes"

    if "no" in text:
        return "No"

    return "Unknown"

# -----------------------------
# SINGLE PROMPT RUN
# -----------------------------

def get_answer(prompt):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = extract_answer(
        response.choices[0].message.content
    )

    return answer, response.usage

# -----------------------------
# SELF CONSISTENCY
# -----------------------------

def self_consistency(prompt):

    answers = []

    total_input_tokens = 0
    total_output_tokens = 0

    for _ in range(5):

        response = client.chat.completions.create(
            model=MODEL,
            temperature=0.7,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        answer = extract_answer(
            response.choices[0].message.content
        )

        answers.append(answer)

        total_input_tokens += (
            response.usage.prompt_tokens
        )

        total_output_tokens += (
            response.usage.completion_tokens
        )

    majority_answer = Counter(
        answers
    ).most_common(1)[0][0]

    return (
        majority_answer,
        total_input_tokens,
        total_output_tokens
    )

# -----------------------------
# MAIN
# -----------------------------

rows = []

with open(
    "scenarios.jsonl",
    "r",
    encoding="utf-8"
) as f:

    for line in f:

        scenario = json.loads(line)

        scenario_id = scenario["id"]
        scenario_text = scenario["scenario"]
        ground_truth = scenario["answer"]

        print(
            f"Running Scenario {scenario_id}"
        )

        # -------------------------
        # DIRECT
        # -------------------------

        direct_prompt = DIRECT_PROMPT.format(
            scenario=scenario_text
        )

        direct_answer, direct_usage = (
            get_answer(direct_prompt)
        )

        direct_correct = (
            direct_answer == ground_truth
        )

        direct_cost = calculate_cost(
            direct_usage.prompt_tokens,
            direct_usage.completion_tokens
        )

        # -------------------------
        # COT
        # -------------------------

        cot_prompt = COT_PROMPT.format(
            scenario=scenario_text
        )

        cot_answer, cot_usage = (
            get_answer(cot_prompt)
        )

        cot_correct = (
            cot_answer == ground_truth
        )

        cot_cost = calculate_cost(
            cot_usage.prompt_tokens,
            cot_usage.completion_tokens
        )

        # -------------------------
        # SELF CONSISTENCY
        # -------------------------

        sc_prompt = SC_PROMPT.format(
            scenario=scenario_text
        )

        (
            sc_answer,
            sc_input_tokens,
            sc_output_tokens
        ) = self_consistency(
            sc_prompt
        )

        sc_correct = (
            sc_answer == ground_truth
        )

        sc_cost = calculate_cost(
            sc_input_tokens,
            sc_output_tokens
        )

        rows.append([
            scenario_id,
            direct_answer,
            direct_correct,
            cot_answer,
            cot_correct,
            sc_answer,
            sc_correct,
            direct_cost,
            cot_cost,
            sc_cost
        ])

# -----------------------------
# SAVE CSV
# -----------------------------

with open(
    "results.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "scenario_id",
        "direct_answer",
        "direct_correct",
        "cot_answer",
        "cot_correct",
        "sc_answer",
        "sc_correct",
        "direct_cost_usd",
        "cot_cost_usd",
        "sc_cost_usd"
    ])

    writer.writerows(rows)

# -----------------------------
# SUMMARY STATS
# -----------------------------

total_direct = sum(
    row[7] for row in rows
)

total_cot = sum(
    row[8] for row in rows
)

total_sc = sum(
    row[9] for row in rows
)

direct_correct_count = sum(
    row[2] for row in rows
)

cot_correct_count = sum(
    row[4] for row in rows
)

sc_correct_count = sum(
    row[6] for row in rows
)

print("\nFinished")
print("results.csv generated")

print("\nTOTAL DIRECT COST:")
print(round(total_direct, 8))

print("\nTOTAL COT COST:")
print(round(total_cot, 8))

print("\nTOTAL SC COST:")
print(round(total_sc, 8))

print("\nDIRECT ACCURACY:")
print(
    f"{direct_correct_count}/15"
)

print("\nCOT ACCURACY:")
print(
    f"{cot_correct_count}/15"
)

print("\nSELF CONSISTENCY ACCURACY:")
print(
    f"{sc_correct_count}/15"
)

print("\nCOST PER CORRECT ANSWER")

print(
    "Direct:",
    round(
        total_direct /
        direct_correct_count,
        8
    )
)

print(
    "CoT:",
    round(
        total_cot /
        cot_correct_count,
        8
    )
)

print(
    "Self Consistency:",
    round(
        total_sc /
        sc_correct_count,
        8
    )
)