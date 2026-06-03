# Prompt Style Evaluation

## Objective

The goal of this experiment was to compare three prompting techniques—Zero-shot, Few-shot, and Role-based prompting—for classifying customer support tickets into predefined categories.

## Accuracy Results

| Style | Accuracy |
|--------|----------|
| Zero-shot | 90.00% |
| Few-shot | 96.67% |
| Role-based | 90.00% |

## Key Findings

- Few-shot prompting achieved the highest accuracy.
- Zero-shot and Role-based prompting achieved the same performance.
- Providing examples helped the model better understand category boundaries and customer intent.
- Role instructions alone were not sufficient to improve classification accuracy.

## Examples Where Few-shot Performed Better

### Example 1

**Ground Truth:** Refund

**Ticket:** Return window elapsed but item is defective.

**Zero-shot Prediction:** Product Quality

**Few-shot Prediction:** Refund

**Role-based Prediction:** Product Quality

The ticket mentioned a defective product, which confused Zero-shot and Role-based prompts. Few-shot correctly identified that the customer's primary intent was requesting a refund.

### Example 2

**Ground Truth:** Refund

**Ticket:** Double charged for subscription.

**Zero-shot Prediction:** Payment

**Few-shot Prediction:** Refund

**Role-based Prediction:** Payment

The ticket involved a billing issue, but the customer explicitly requested a refund. Few-shot handled this intent better.

## Common Misclassification

### Example

**Ground Truth:** Shipping

**Ticket:** Wrong address entered by mistake.

**Predictions:**
- Zero-shot: Order Change
- Few-shot: Order Change
- Role-based: Order Change

The ticket requested an address modification before shipment. All prompting styles interpreted the request as an Order Change instead of Shipping.

## Conclusion

Few-shot prompting achieved the best overall performance with an accuracy of 96.67%.

The examples included in the prompt helped the model focus on customer intent rather than individual keywords. Zero-shot and Role-based prompting both achieved 90.00% accuracy and made similar mistakes, particularly when tickets contained overlapping concepts such as refunds, payments, product quality issues, and order modifications.

For customer support ticket classification tasks, Few-shot prompting is the most effective approach because example-based guidance reduces ambiguity and improves consistency.