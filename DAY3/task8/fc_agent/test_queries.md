# Test Queries

## Single Tool Queries

### Query 1

What's the shipping status of order ORD-1002?

Expected Tool:
get_shipping

---

### Query 2

Show details for order ORD-1005.

Expected Tool:
get_order

---

### Query 3

What is the refund policy for electronics?

Expected Tool:
check_refund_policy

---

## Multi-Tool Queries

### Query 4

Order ORD-1005 was delivered. Can I get a refund?

Expected Tools:
get_order → check_refund_policy

---

### Query 5

My order ORD-1002 is delayed. What's happening?

Expected Tools:
get_shipping

---

### Query 6

Tell me about ORD-1003 and whether I can get a refund.

Expected Tools:
get_order → check_refund_policy

---

## Multi-Turn Conversations

### Query 7

Where is my order ORD-1008?

Follow-up:
When should it arrive?

Expected Tool:
get_shipping

---

### Query 8

Show details for ORD-1014.

Follow-up:
Can I return it?

Expected Tools:
get_order → check_refund_policy

---

## Escalation Queries

### Query 9

I'm extremely angry. Nobody is helping me.

Expected Tool:
escalate_to_human

---

### Query 10

I want to speak to a manager immediately.

Expected Tool:
escalate_to_human
