# Learnings from Prompt Chaining

## Objective

The goal of this task was to compare a chained prompting workflow against a single large prompt by splitting the process into smaller and more focused steps.

The pipeline consisted of:

1. Extract structured attributes from a product brief.
2. Generate advertisement variants from the extracted attributes.
3. Select the best advertisement using predefined brand rules.

---

## What Worked Well

### Step 1: Attribute Extraction

The extraction step successfully converted unstructured product descriptions into structured JSON objects.

Example:

* Product Name
* Category
* Key Features
* Target Audience

This structured representation made the following steps more predictable and easier to control.

---

### Step 2: Advertisement Generation

Using the structured attributes produced by Step 1 resulted in more focused advertisement copy.

The model consistently used the extracted features and target audience information when generating marketing content.

Because the generation step only needed to focus on copywriting, the outputs were generally relevant and concise.

---

### Step 3: Advertisement Selection

The selection step successfully evaluated the generated advertisements against predefined brand rules.

The model was able to identify advertisements that:

* Avoided prohibited superlatives
* Maintained a professional tone
* Highlighted actual product benefits
* Followed brand compliance requirements

This added an additional quality-control stage to the workflow.

---

## What Broke During Testing

The main failure point in the pipeline was Step 1.

If incorrect attributes were extracted, the error propagated to later stages.

Examples:

* Incorrect product category
* Missing product features
* Incorrect target audience

When these errors occurred, Step 2 generated advertisements using incorrect information.

Step 3 could still choose the best advertisement among the generated options, but it could not correct factual mistakes introduced earlier in the pipeline.

This demonstrated how errors can propagate through chained systems.

---

## Impact of Step 1 Errors on Step 2

Step 2 depends entirely on the output of Step 1.

If Step 1 extracted incomplete or incorrect information:

* Advertisement quality decreased.
* Important product features were omitted.
* Messaging became less relevant to the intended audience.

The generation stage cannot recover information that was never extracted.

---

## Lessons Learned

Splitting a complex task into multiple focused prompts improves reliability and makes debugging easier.

Advantages observed:

* Clear separation of responsibilities.
* Easier error identification.
* Structured intermediate outputs.
* Better controllability.
* Simpler prompt design.

The intermediate files generated at each stage made it easy to determine where mistakes occurred.

In a single large prompt, it would be much harder to identify which part of the process failed.

---

## Conclusion

Prompt chaining provides a structured workflow where each step focuses on a single responsibility.

Although errors can propagate from earlier stages, the approach offers greater transparency, easier debugging, and better control compared to solving the entire task with one large prompt.
