# Accuracy Summary

## Overall Results

A total of 10 synthetic invoice documents were processed using Gemini 2.5 Flash with response_schema and Pydantic validation.

The extraction achieved 100% field-level accuracy across all evaluated fields.

## Per-Field Accuracy

| Field          | Accuracy |
| -------------- | -------- |
| invoice_number | 100%     |
| invoice_date   | 100%     |
| supplier_name  | 100%     |
| customer_name  | 100%     |
| total_amount   | 100%     |
| status         | 100%     |
| notes          | 100%     |

## Common Errors

No extraction errors were observed during testing because the sample invoices followed a consistent format.

## Observations

* Gemini performed very well when constrained with response_schema.
* Pydantic validation ensured the output matched the required structure.
* Optional fields such as notes were handled correctly when absent.
* Enum values (PAID, UNPAID, OVERDUE) were extracted accurately.

## Improvements

To better evaluate robustness, future testing should include:

* OCR-based scanned invoices
* Handwritten invoices
* Missing fields
* Different invoice layouts
* Noisy or partially corrupted documents
