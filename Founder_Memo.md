# Founder Memo: COD Risk Reduction Strategy

**To:** Founder, Oytra  
**Subject:** Reducing COD Returns Through Risk-Based Order Decisions  
**Date:** 30 October 2026

## 1. Executive Summary

Oytra's COD orders create a significant operational cost because returned-to-origin (RTO) orders incur forward shipping, return shipping, packaging and handling costs. The proposed decision engine classifies orders into four actions: Ship as-is, Ship after WhatsApp confirmation, Nudge to prepaid, and Hold-cancel.

The goal is to reduce avoidable RTO costs without unnecessarily rejecting genuine customers who prefer Cash on Delivery.

## 2. Key Findings from the Dataset

The supplied historical dataset contains approximately 2,018 order records. After normalizing status labels, the initial analysis showed:

- Approximately 28.4% of completed orders were marked as RTO.
- First-time customers had an observed RTO rate of approximately 30.3%.
- Customers with two previous RTOs had an observed RTO rate of approximately 76.5%. This group contained only 34 orders, so the result should be treated cautiously.
- Gorakhpur and Darbhanga showed comparatively high observed RTO rates of approximately 63% and 58.1%, respectively. These city-level patterns need more data before being used as cancellation rules.

These findings suggest that previous RTO history can be a useful risk signal. However, location and customer history should not be treated as proof that an individual order is fraudulent.

## 3. Proposed Decision Rules

The prototype uses editable thresholds in `config.json` and assigns one of four actions:

1. **Hold-cancel:** Customer has reached the configured high-risk previous-RTO threshold.
2. **Ship after WhatsApp confirmation:** The order has text-quality warnings, previous RTO history, or is from a first-time customer.
3. **Nudge to prepaid:** The order value reaches the configured high-value threshold.
4. **Ship as-is:** No configured risk condition is triggered.

The current prototype uses basic rule-based name and address checks. It does not connect to an LLM or a live WhatsApp service. These checks are review signals, not proof of fake details.

## 4. Financial Impact Estimate

The estimated cost of one RTO is:

| Cost component | Amount |
|---|---:|
| Forward shipping | ₹65 |
| Return shipping | ₹65 |
| Packaging and handling | ₹25 |
| Expected damage cost (8% × ₹180) | ₹14.40 |
| **Total estimated RTO cost** | **₹169.40** |

In the prototype's historical simulation, orders classified as Hold-cancel included:

- 26 historical RTO orders, representing a potential RTO cost avoidance of ₹4,404.40.
- 8 historical Delivered orders, representing