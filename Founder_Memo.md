# Founder Memo: COD Risk Decision Engine

## 1. Executive Summary

The objective of this decision engine is to reduce Return to Origin (RTO) losses without unnecessarily rejecting genuine COD customers.

The historical dataset contains 2,018 orders from April to September 2026. It records 1,444 delivered orders, 573 RTO orders and 1 in-transit order. The overall RTO rate among completed orders is approximately 28.4%.

My recommendation is to use a risk-based approach: confirm uncertain orders, encourage prepaid payment for selected orders, and avoid automatic cancellation unless there is strong evidence of repeated RTO behaviour.

## 2. Key Dataset Findings

Three useful patterns from the historical data are:

- **Overall RTO:** 573 out of 2,017 completed orders were returned, giving an RTO rate of approximately 28.4%.
- **First-time customers:** The preliminary analysis showed an RTO rate of approximately 30.3%. This suggests that first-time customers should not automatically be treated as risky.
- **Repeated RTO history:** Customers with two previous RTOs showed an RTO rate of approximately 76.5% in a small group of 34 orders. This is a strong warning signal, but the small sample size means it should be monitored before making automatic cancellation decisions.

The preliminary city-level analysis also showed higher RTO rates in Gorakhpur (63%) and Darbhanga (58.1%). These city-level patterns should be treated as indicators for further monitoring, not as reasons to reject every order from those locations.

## 3. Recommended Decision Rules

The engine uses four possible actions:

- **Ship as-is:** For orders without major risk signals.
- **Ship after WhatsApp confirmation:** For first-time customers, uncertain address/name details or customers with some previous RTO history.
- **Nudge to prepaid:** For selected higher-value orders, offering a 5% prepaid discount.
- **Hold/cancel:** For customers with two or more previous RTOs, subject to monitoring and review.

The thresholds are editable in the application configuration. The current name and address checks are basic rule-based checks; they do not prove that a customer or address is fake.

## 4. Financial Trade-off

The estimated cost of one RTO is INR 169.40:

- Forward shipping: INR 65
- Return shipping: INR 65
- Packaging and handling: INR 25
- Expected damage cost: INR 14.40

The damage estimate is based on 8% of returned items being unresellable at an average product cost of INR 180.

The business should balance this cost against the delivered gross margin and customer acquisition cost. The stated customer acquisition cost is INR 300 or more, so cancelling genuine first-time customers can also create a business loss.

My recommendation is to prioritise confirmation and prepaid nudges before cancellation. This protects genuine customers while helping reduce avoidable RTO costs.

## 5. September 2026 Retrospective Simulation

After removing duplicate order IDs, the September 2026 dataset contains 329 unique orders.

The decision engine classified them as:

| Decision | Orders |
|---|---:|
| Ship as-is | 44 |
| Ship after WhatsApp confirmation | 262 |
| Nudge to prepaid | 20 |
| Hold/cancel | 3 |

All three orders in the hold/cancel category had historically ended in RTO. At an estimated RTO cost of INR 169.40 per order, the potential RTO cost avoidance is INR 508.20.

No historically delivered orders were placed in the hold/cancel category. Therefore, the estimated genuine-order gross margin loss is INR 0, and the estimated net impact is positive INR 508.20.

These are retrospective estimates based on historical outcomes. They are not proof of actual savings or guaranteed future results.

## 6. Risks and Monitoring

Some genuine customers may have incomplete addresses or unusual names. A rule-based system could incorrectly flag them.

To reduce this risk:

- Use WhatsApp confirmation before cancellation where possible.
- Monitor false positives and customer responses.
- Review city-level patterns regularly rather than blocking locations.
- Track prepaid conversion and the effect of the discount.
- Keep automatic cancellation limited until the rules have been tested with live results.

The WhatsApp flow in this prototype is simulated; it is not connected to a real WhatsApp account. The current prototype also uses rule-based checks rather than a live LLM service.

## 7. Next Two Weeks

**Week 1:** Test the decision engine on historical orders, review flagged orders and verify the confirmation messages in English and Telugu.

**Week 2:** Run a small monitored pilot, compare confirmation responses, prepaid conversions and RTO outcomes, and adjust thresholds based on the results.

## Final Recommendation

Do not automatically cancel all risky COD orders. Start with WhatsApp confirmation and prepaid nudges, and reserve hold/cancel for stronger risk signals. This approach gives the business a better balance between reducing RTO costs and protecting genuine customers.