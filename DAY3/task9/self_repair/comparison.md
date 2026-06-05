# Comparison: Without Repair vs With Repair

## Without Repair

Success Rate:

10 / 20

50%

---

## With Repair

Success Rate:

20 / 20

100%

---

## Improvement

The self-repair loop improved extraction accuracy from 50% to 100%.

Absolute Improvement:

50 percentage points

---

## Common Errors Fixed

* Invalid email addresses
* Invalid phone numbers
* OCR-related phone number errors
* Missing pincodes
* Missing address information
* Formatting inconsistencies

---

## Cost vs Success Rate Trade-off

The repair loop required additional model calls whenever validation failed. This increased token consumption and API usage compared to a single extraction attempt.

However, the additional cost resulted in a substantial improvement in reliability. All validation failures were corrected through one retry, increasing the final success rate from 50% to 100%.

---

## Conclusion

The self-repair mechanism proved highly effective for structured data extraction.

When validation errors occurred, the system automatically supplied the model with its previous output and the exact validation error message. This allowed the model to correct mistakes and regenerate schema-compliant JSON.

The experiment demonstrated that validation-guided retries can dramatically improve extraction quality, increasing successful extractions from 50% to 100% across the evaluation dataset.
