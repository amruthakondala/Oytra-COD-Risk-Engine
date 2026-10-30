# AI Usage Log - Oytra COD Decision Engine

## 1. AI Tool Used

ChatGPT was used as an assistance tool during project development.

## 2. How AI Was Used

AI assistance was used for:

- Understanding the assignment requirements.
- Planning the project structure and features.
- Getting guidance on Python, Pandas, and Streamlit.
- Debugging code and resolving errors.
- Reviewing decision rules and financial calculations.
- Preparing project documentation and the founder memo.

## 3. Examples of Weak or Incorrect AI-Assisted Output

### Example 1: Using only the latest date

An initial memo section focused on the 9 orders from the latest date in the dataset. However, the assignment asked what the decision engine would have done to last month's orders.

**How it was corrected:** I checked the order dates in PowerShell and identified September 2026 as the latest complete month. I then ran the decision rules on all September orders.

### Example 2: Duplicate orders in monthly counts

The initial monthly count showed 334 September records. This did not account for duplicate order IDs.

**How it was corrected:** I checked the data after sorting by order date and removing duplicate order IDs. The final September analysis used 329 unique orders.

### Example 3: Presenting estimated savings

An initial financial summary could be misunderstood as actual money saved by the business.

**How it was corrected:** I labelled the figures as potential RTO cost avoidance and estimated net impact. I also added a note explaining that these are retrospective estimates, not actual or guaranteed savings.

## 4. Human Decisions and Verification

I reviewed the decision rules, checked the dataset dates and monthly counts using PowerShell, and verified the September decision summary. I also reviewed the financial assumptions and documented the limitations of the prototype.

## 5. Limitations

- No LLM API is connected to the application.
- Order classification uses rule-based logic.
- WhatsApp interactions are simulated.
- Financial impact figures are estimates based on the assignment assumptions.

## 6. Transparency

AI was used to support development, debugging, and documentation. The final implementation and its limitations were reviewed, and simulated results are not presented as real-world outcomes.