import warnings
warnings.filterwarnings("ignore")

import os
import json

from google import genai
from pydantic import ValidationError

from schema import ContactCard

# --------------------------
# GEMINI CLIENT
# --------------------------

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL = "gemini-2.5-flash"

MAX_RETRIES = 3


# --------------------------
# REPAIR FUNCTION
# --------------------------

def extract_contact(
    document_text
):

    prompt = f"""
You are an information extraction system.

Extract contact information from the provided text.

Requirements:
- Return only valid JSON.
- Follow the ContactCard schema exactly.
- Do not invent missing information.
- If a field is unavailable, use null where allowed.
- Ensure email addresses are valid.
- Ensure phone numbers contain exactly 10 digits.
- Ensure address contains city and pincode.

Text:

{document_text}
"""

    retries = 0
    errors_seen = []

    while retries <= MAX_RETRIES:

        print(
            f"\n========== ATTEMPT {retries + 1} =========="
        )

        response = (
            client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config={
                    "response_mime_type":
                    "application/json",

                    "response_schema":
                    ContactCard
                }
            )
        )

        print(
            "\nModel Output:"
        )

        print(
            response.text
        )

        try:

            contact = (
                ContactCard
                .model_validate_json(
                    response.text
                )
            )

            print(
                "\nVALID OUTPUT"
            )

            print(
                json.dumps(
                    contact.model_dump(),
                    indent=4
                )
            )

            return {
                "contact":
                contact.model_dump(),

                "retries":
                retries,

                "final_valid":
                True,

                "errors_seen":
                errors_seen
            }

        except ValidationError as e:

            error_msg = str(e)

            errors_seen.append(
                error_msg
            )

            print(
                "\nVALIDATION ERROR:"
            )

            print(
                error_msg
            )

            retries += 1

            if retries > MAX_RETRIES:

                print(
                    "\nMAX RETRIES EXCEEDED"
                )

                return {
                    "contact":
                    None,

                    "retries":
                    retries,

                    "final_valid":
                    False,

                    "errors_seen":
                    errors_seen
                }

            prompt = f"""
You previously generated JSON that failed validation.

Original Text:

{document_text}

Previous JSON:

{response.text}

Validation Errors:

{error_msg}

Instructions:

- Correct only the validation errors.
- Preserve all valid fields.
- Return only valid JSON.
- Do not add explanations.
- Follow the ContactCard schema exactly.
- Ensure email format is valid.
- Ensure phone number contains exactly 10 digits.
- Ensure city and pincode are present.

Return corrected JSON.
"""


# --------------------------
# TEST SINGLE FILE
# --------------------------

if __name__ == "__main__":

    with open(
        "inputs/input_6.txt",
        "r",
        encoding="utf-8"
    ) as f:

        text = f.read()

    result = extract_contact(
        text
    )

    print(
        "\n========== FINAL RESULT =========="
    )

    print(
        json.dumps(
            result,
            indent=4
        )
    )