import warnings
warnings.filterwarnings("ignore")

import os
import sys
import json

from google import genai
from pydantic import ValidationError

from schema import Invoice

# --------------------------
# GEMINI CLIENT
# --------------------------

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL = "gemini-2.5-flash"

# --------------------------
# EXTRACTION FUNCTION
# --------------------------

def extract_invoice(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:

        document_text = f.read()

    prompt = f"""
Extract invoice information
from the following document.

Return data matching the
provided schema exactly.

Document:

{document_text}
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config={
            "response_mime_type":
            "application/json",
            "response_schema":
            Invoice
        }
    )

    try:

        invoice = Invoice.model_validate_json(
            response.text
        )

        return invoice.model_dump()

    except ValidationError as e:

        print(
            "Validation Error:"
        )

        print(e)

        return None


# --------------------------
# CLI MODE
# --------------------------

if __name__ == "__main__":

    if len(sys.argv) != 2:

        print(
            "Usage: python main.py <file_path>"
        )

        sys.exit()

    result = extract_invoice(
        sys.argv[1]
    )

    if result:

        print(
            json.dumps(
                result,
                indent=4
            )
        )