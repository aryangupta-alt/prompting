import json
from typing import Dict, Any

# -------------------------
# LOAD ORDERS
# -------------------------

with open(
    "fake_orders.json",
    "r",
    encoding="utf-8"
) as f:

    ORDERS = json.load(f)

# -------------------------
# TOOL 1
# -------------------------

def get_order(order_id: str) -> Dict[str, Any]:

    for order in ORDERS:

        if order["order_id"] == order_id:

            return {
                "order_id":
                order["order_id"],

                "customer":
                order["customer"],

                "product":
                order["product"],

                "category":
                order["category"],

                "status":
                order["status"]
            }

    return {
        "error":
        "Order not found"
    }

# -------------------------
# TOOL 2
# -------------------------

def get_shipping(order_id: str) -> Dict[str, Any]:

    for order in ORDERS:

        if order["order_id"] == order_id:

            return {
                "order_id":
                order["order_id"],

                "shipping_status":
                order["shipping_status"]
            }

    return {
        "error":
        "Order not found"
    }

# -------------------------
# TOOL 3
# -------------------------

def check_refund_policy(
    category: str
) -> Dict[str, Any]:

    policies = {

        "electronics":
        "Refund allowed within 7 days if product is unused.",

        "clothing":
        "Refund allowed within 30 days with tags attached.",

        "books":
        "Refund allowed only for damaged items.",

        "furniture":
        "Refund allowed within 14 days."
    }

    return {
        "category":
        category,

        "policy":
        policies.get(
            category.lower(),
            "No refund policy found."
        )
    }

# -------------------------
# TOOL 4
# -------------------------

def escalate_to_human(
    reason: str
) -> Dict[str, Any]:

    return {
        "status":
        "Escalated",

        "message":
        "A human support agent will contact you shortly.",

        "reason":
        reason
    }