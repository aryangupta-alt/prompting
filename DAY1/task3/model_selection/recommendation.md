# Model Selection Recommendation

## Objective

The objective of this experiment was to compare three Large Language Models (LLMs) on the task of summarizing documents into exactly three bullet points. The comparison was based on latency, token usage, cost, and output quality.

## Models Evaluated

1. openai/gpt-oss-120b
2. meta-llama/llama-4-scout-17b-16e-instruct
3. allam-2-7b

## Evaluation Criteria

* Latency (response time in milliseconds)
* Input Tokens
* Output Tokens
* Cost per request
* Quality Score (1–5 using LLM-as-Judge)

## Observations

### openai/gpt-oss-120b

Strengths:

* Produced the most detailed and accurate summaries.
* Consistently achieved the highest quality scores.
* Better at preserving important information from the original document.

Weaknesses:

* Highest latency among the tested models.
* Highest cost per request.

Best Use Cases:

* High-stakes business applications.
* Legal, financial, or healthcare document summarization.
* Tasks requiring maximum quality and accuracy.

### meta-llama/llama-4-scout-17b-16e-instruct

Strengths:

* Good balance between quality and speed.
* Lower cost than GPT-OSS-120B.
* Generated concise and accurate summaries.

Weaknesses:

* Slightly less detailed than GPT-OSS-120B.

Best Use Cases:

* Production applications.
* Customer support systems.
* Business reporting and analytics.

### allam-2-7b

Strengths:

* Fastest model tested.
* Lowest operational cost.
* Suitable for high-volume workloads.

Weaknesses:

* Lower quality scores.
* Occasionally omitted important information.

Best Use Cases:

* Large-scale batch processing.
* Internal tools.
* Low-risk summarization tasks.

## Recommended Model

### Recommendation: meta-llama/llama-4-scout-17b-16e-instruct

The Llama-4 Scout model is recommended because it provides the best balance between quality, latency, and cost. While GPT-OSS-120B produced slightly higher-quality summaries, the improvement was not significant enough to justify the additional latency and cost for most business applications.

Llama-4 Scout delivered strong summarization performance while remaining fast and cost-effective, making it the most practical choice for real-world deployment.

## Decision Rule

| Task Type                            | Recommended Model                         |
| ------------------------------------ | ----------------------------------------- |
| High quality, high accuracy required | openai/gpt-oss-120b                       |
| Balanced quality and cost            | meta-llama/llama-4-scout-17b-16e-instruct |
| High volume, low cost, low risk      | allam-2-7b                                |

## Conclusion

For document summarization tasks, meta-llama/llama-4-scout-17b-16e-instruct offers the best overall trade-off between speed, cost, and quality. Therefore, it is the recommended model for most production use cases.
