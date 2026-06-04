import os
import json
import re

from groq import Groq

from tools import (
    get_order,
    get_shipping,
    check_refund_policy,
    escalate_to_human
)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = "llama-3.3-70b-versatile"


def run_agent(user_message):

    prompt = """
You are a customer support agent.

Available tools:

1. get_order(order_id)
   - Returns order details including customer, product, category, and order status.

2. get_shipping(order_id)
   - Returns shipping information for an order.

3. check_refund_policy(category)
   - Returns the refund policy for a product category.

4. escalate_to_human(reason)
   - Escalates the conversation to a human support representative.

Important Rules:

- Never invent or guess arguments.
- If information required for a tool is missing, first call another tool to obtain it.
- If a user asks about refunds and provides only an order ID, you MUST first call get_order(order_id) to retrieve the product category.
- Only after obtaining the category should you call check_refund_policy(category).
- If a customer is angry, abusive, requests a manager, or reports repeated unresolved issues, use escalate_to_human.
- For shipping questions, use get_shipping(order_id).
- For order details, use get_order(order_id).
- Multi-step problems may require multiple tool calls.
- Return ONLY valid JSON.
- Do not use markdown.
- Do not use triple backticks.
- Do not explain anything.

Output Format:

{
    "tool": "<tool_name>",
    "args": {}
}

Examples:

Customer:
What's the shipping status of ORD-1002?

Output:
{
    "tool":"get_shipping",
    "args":{
        "order_id":"ORD-1002"
    }
}

Customer:
Show details for ORD-1005

Output:
{
    "tool":"get_order",
    "args":{
        "order_id":"ORD-1005"
    }
}

Customer:
Order ORD-1005 was delivered. Can I get a refund?

Output:
{
    "tool":"get_order",
    "args":{
        "order_id":"ORD-1005"
    }
}

Customer Message:
""" + user_message

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    tool_call = response.choices[0].message.content

    print("\nTool Decision:")
    print(tool_call)

    tool_call = tool_call.replace(
        "```json",
        ""
    )

    tool_call = tool_call.replace(
        "```",
        ""
    )

    tool_call = tool_call.strip()

    try:

        decision = json.loads(
            tool_call
        )

        tool_name = decision["tool"]

        args = decision["args"]

    except Exception as e:

        print(
            "\nCould not determine tool."
        )

        print(e)

        return

    #    # -------------------
    # MULTI-STEP REFUND LOGIC
    # -------------------

    if (
        "refund" in user_message.lower()
        and "ORD-" in user_message.upper()
    ):

        match = re.search(
            r"ORD-\d+",
            user_message,
            re.IGNORECASE
        )

        if match:

            order_id = match.group().upper()

            order_info = get_order(
                order_id
            )

            print(
                "\nTool Called: get_order"
            )

            print(
                order_info
            )

            category = order_info.get(
                "category"
            )

            if category:

                refund_info = (
                    check_refund_policy(
                        category
                    )
                )

                print(
                    "\nTool Called: check_refund_policy"
                )

                print(
                    refund_info
                )

                result = {
                    "order_info":
                    order_info,

                    "refund_policy":
                    refund_info
                }

            else:

                result = {
                    "error":
                    "Category not found"
                }

        else:

            result = {
                "error":
                "Order ID not found"
            }

    else:

        # -------------------
        # NORMAL TOOL EXECUTION
        # -------------------

        if tool_name == "get_order":

            result = get_order(
                **args
            )

        elif tool_name == "get_shipping":

            result = get_shipping(
                **args
            )

        elif tool_name == "check_refund_policy":

            result = check_refund_policy(
                **args
            )

        elif tool_name == "escalate_to_human":

            result = escalate_to_human(
                **args
            )

        else:

            result = {
                "error":
                "Unknown tool"
            }

    print("\nTool Result:")
    print(result)

    # -------------------
    # FINAL RESPONSE
    # -------------------

    final_prompt = f"""
Customer Message:
{user_message}

Tool Result:
{json.dumps(result, indent=2)}

Generate a concise customer support response.

Rules:
- Maximum 3 sentences.
- Use the tool result.
- Do not mention internal tools.
- Be direct and helpful.
"""

    final_response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": final_prompt
            }
        ],
        temperature=0
    )

    print("\nFinal Response:")
    print(
        final_response
        .choices[0]
        .message
        .content
    )


if __name__ == "__main__":

    while True:

        query = input(
            "\nCustomer: "
        )

        if query.lower() == "exit":

            break

        run_agent(query)