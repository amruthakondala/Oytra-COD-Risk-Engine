# Decision Log – Oytra COD Decision Engine

## 1. Project Goal

The goal is to reduce COD Return to Origin (RTO) losses while avoiding unnecessary cancellations of genuine customer orders.

## 2. Decisions Made

### Decision 1: Previous RTO History
- Customers with 2 or more previous RTOs are classified as Hold-cancel.
- Customers with 1 previous RTO are asked for WhatsApp confirmation.

**Reason:** Previous RTO history can help identify customers with higher delivery risk.

### Decision 2: First-time Customers
- Customers with no previous orders are classified as Ship after WhatsApp confirmation.

**Reason:** First-time customers may need additional confirmation, but their orders should not be cancelled automatically.

### Decision 3: High-value Orders
- Orders worth ₹1,000 or more are classified as Nudge to prepaid if they do not meet a higher-risk rule.

**Reason:** Encouraging prepaid payment may reduce COD-related delivery risk.

### Decision 4: Other Orders
- Orders that do not meet the above conditions are classified as Ship as-is.

**Reason:** Lower-risk orders should not face unnecessary confirmation steps.

## 3. WhatsApp Simulation

- Customers can receive a confirmation message in English or Telugu.
- Possible responses are YES, NO, Random Reply, and No Reply.
- A 5% prepaid discount is used in the simulation.
- The simulator does not send real WhatsApp messages.

## 4. Financial Assumptions

The financial dashboard uses the following assignment assumptions:

- Forward shipping: ₹65
- Return shipping: ₹65
- Packaging and handling: ₹25
- Damage rate: 8%
- Average product cost: ₹180
- Gross margin on delivered orders: 62%

Estimated RTO cost:

₹65 + ₹65 + ₹25 + (8% × ₹180) = ₹169.40

## 5. Limitations

- The current decision engine uses rule-based classification.
- The current version does not connect to an LLM API.
- WhatsApp messages and customer responses are simulated.
- Financial impact is a historical estimate, not confirmed savings.
- The rules and thresholds need further validation before real business use.

## 6. Future Improvements

- Add LLM-based analysis for ambiguous addresses and customer names.
- Integrate a real WhatsApp messaging service.
- Validate decisions using a larger historical dataset.
- Monitor false cancellations and actual RTO reduction.
- Improve the dashboard with daily operational reporting.