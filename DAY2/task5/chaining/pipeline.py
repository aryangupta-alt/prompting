from groq import Groq
import os
import json

# -----------------------------
# CONFIG
# -----------------------------

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = "openai/gpt-oss-120b"

# -----------------------------
# LOAD PROMPTS
# -----------------------------

with open("prompts/extract.txt", "r") as f:
    EXTRACT_PROMPT = f.read()

with open("prompts/generate.txt", "r") as f:
    GENERATE_PROMPT = f.read()

with open("prompts/select.txt", "r") as f:
    SELECT_PROMPT = f.read()

# -----------------------------
# CALL MODEL
# -----------------------------

def call_llm(prompt):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content

# -----------------------------
# PROCESS 5 BRIEFS
# -----------------------------

for i in range(1, 6):

    print(f"\nProcessing Brief {i}")

    run_folder = f"runs/run{i}"

    os.makedirs(
        run_folder,
        exist_ok=True
    )

    # -------------------------
    # READ BRIEF
    # -------------------------

    with open(
        f"briefs/brief{i}.txt",
        "r",
        encoding="utf-8"
    ) as f:

        brief = f.read()

    # Save original brief

    with open(
        f"{run_folder}/input_brief.txt",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(brief)

    # -------------------------
    # STEP 1: EXTRACT
    # -------------------------

    extract_prompt = EXTRACT_PROMPT.format(
        brief=brief
    )

    attributes = call_llm(
        extract_prompt
    )

    with open(
        f"{run_folder}/step1_attributes.json",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(attributes)

    # -------------------------
    # STEP 2: GENERATE
    # -------------------------

    generate_prompt = GENERATE_PROMPT.format(
        attributes=attributes
    )

    variants = call_llm(
        generate_prompt
    )

    with open(
        f"{run_folder}/step2_variants.json",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(variants)

    # -------------------------
    # STEP 3: SELECT
    # -------------------------

    select_prompt = SELECT_PROMPT.format(
        variants=variants
    )

    winner = call_llm(
        select_prompt
    )

    with open(
        f"{run_folder}/step3_winner.json",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(winner)

    print(
        f"Completed Brief {i}"
    )

print("\nPipeline Finished")