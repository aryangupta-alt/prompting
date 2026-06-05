import csv
import os
import time

from repair_loop import extract_contact

INPUT_FOLDER = "inputs"

rows = []

for i in range(1, 21):

    file_name = f"input_{i}.txt"

    file_path = os.path.join(
        INPUT_FOLDER,
        file_name
    )

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            text = f.read()

        result = extract_contact(
            text
        )

        retries = result[
            "retries"
        ]

        valid = result[
            "final_valid"
        ]

        errors_seen = (
            "; ".join(
                result["errors_seen"]
            )
            if result["errors_seen"]
            else "None"
        )

        rows.append(
            [
                f"input_{i}",

                retries == 0,

                valid,

                retries,

                errors_seen,

                0
            ]
        )

        print(
            f"Processed input_{i}"
        )

    except Exception as e:

        print(
            f"Failed input_{i}: {e}"
        )

        rows.append(
            [
                f"input_{i}",

                False,

                False,

                3,

                str(e),

                0
            ]
        )

    # Gemini free-tier rate limit protection
    time.sleep(12)

# -----------------------
# SAVE RESULTS
# -----------------------

with open(
    "results.csv",
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(f)

    writer.writerow(
        [
            "input_id",
            "first_try_valid",
            "final_valid",
            "num_retries",
            "errors_seen",
            "total_cost"
        ]
    )

    writer.writerows(
        rows
    )

print(
    "\nresults.csv generated successfully"
)