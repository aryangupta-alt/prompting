import warnings

warnings.filterwarnings("ignore")

import json
import csv
import os

from main import extract_invoice


# --------------------
# LOAD GROUND TRUTH
# --------------------

ground_truth = {}

with open(
    "ground_truth.jsonl",
    "r",
    encoding="utf-8"
) as f:

    for line in f:

        record = json.loads(line)

        ground_truth[
            record["sample_id"]
        ] = record


rows = []

# --------------------
# RUN ALL SAMPLES
# --------------------

for i in range(1, 11):

    sample_id = f"invoice_{i}"

    file_path = (
        f"samples/{sample_id}.txt"
    )

    extracted = extract_invoice(
        file_path
    )

    truth = ground_truth[
        sample_id
    ]

    fields = [
        "invoice_number",
        "invoice_date",
        "supplier_name",
        "customer_name",
        "total_amount",
        "status",
        "notes"
    ]

    for field in fields:

        extracted_value = (
            extracted.get(field)
        )

        truth_value = (
            truth.get(field)
        )

        match = (
            extracted_value ==
            truth_value
        )

        rows.append([
            sample_id,
            field,
            extracted_value,
            truth_value,
            match
        ])


# --------------------
# SAVE CSV
# --------------------

with open(
    "field_accuracy.csv",
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(f)

    writer.writerow([
        "sample_id",
        "field_name",
        "extracted_value",
        "ground_truth_value",
        "exact_match"
    ])

    writer.writerows(rows)

print(
    "field_accuracy.csv generated"
)