# Decision Log - Oytra COD Decision Engine

## 1. Project Goal

The goal is to reduce COD Return to Origin (RTO) losses while avoiding unnecessary cancellations of genuine customer orders.

## 2. Decisions Made

### Decision 1: Previous RTO History
- Customers with 2 or more previous RTOs are classified as Hold/cancel.
- Customers with 1 previous RTO are asked for WhatsApp confirmation.

**Reason:** Previous RTO history can help identify customers with higher delivery risk.

### Decision 2: Name and Address Checks
- Very short names, names containing digits, and short or missing addresses are flagged for WhatsApp confirmation.

**Reason:** These checks help identify details that may need review. They do not prove that a customer or address is fake.

### Decision 3: First-time Customers
- Customers with no previous orders are classified as Ship after WhatsApp confirmation.

**Reason:** First-time customers may be genuine, so they should not be automatically cancelled.

### Decision 4: High-value Orders
- Orders worth INR 1,000 or more are classified as Nudge to prepaid if they do not meet a higher-priority rule.

**Reason:** Encouraging prepaid payment may reduce COD-related delivery risk.

### Decision 5: Other Orders
- Orders that do not meet the above conditions are classified as Ship as-is.

**Reason:** Lower-risk orders should not face unnecessary confirmation steps.

## 3. Alternatives Considered

- **Cancel all COD orders with risk signals:** Not selected because genuine customers may be rejected.
- **Use only order value to identify risk:** Not selected because order value alone does not show customer delivery behaviour.
- **Ask every customer for confirmation:** Not selected because it could add unnecessary friction for lower-risk orders.
- **Use previous RTO history with confirmation checks:** Selected because it balances RTO reduction with customer experience.

## 4. WhatsApp Simulation

- Customers can receive a confirmation message in English or Telugu.
- Possible responses are YES, NO, Random Reply, and No Reply.
- A 5% prepaid discount is used in the simulation.
- The simulator does not send real WhatsApp messages.

## 5. Financial Assumptions

The financial dashboard uses the assignment assumptions:

- Forward shipping: INR 65
- Return shipping: INR 65
- Packaging and handling: INR 25
- Damage rate: 8%
- Average product cost: INR 180
- Gross margin on delivered orders: 62%

Estimated RTO cost:

INR 65 + INR 65 + INR 25 + (8% × INR 180) = INR 169.40

## 6. Limitations

- The current decision engine uses rule-based classification.
- The current version does not connect to an LLM API.
- WhatsApp messages and customer responses are simulated.
- Financial impact is a historical estimate, not confirmed savings.
- The rules and thresholds need further validation before real business use.

## 7. Future Improvements

- Add LLM-based analysis for ambiguous addresses and customer names.
- Integrate a real WhatsApp messaging service.
- Validate decisions using a larger historical dataset.
- Monitor false cancellations and actual RTO reduction.
- Improve the dashboard with daily operational reporting.