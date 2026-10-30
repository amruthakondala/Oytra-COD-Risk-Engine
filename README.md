# Oytra COD Order Decision Engine

## Project Overview

This project helps a D2C haircare brand identify risky Cash on Delivery (COD) orders and make better shipping decisions.

It analyses historical order data and classifies each order into one of four categories:

- Ship as-is
- Ship after WhatsApp confirmation
- Nudge to prepaid
- Hold-cancel

## Features

### 1. COD Order Analysis
- Upload historical orders through a CSV file.
- View order status and RTO statistics.
- Analyse customer order history and previous RTOs.

### 2. Order Decision Engine
- Applies configurable rules to classify orders.
- Displays a decision and a plain-English reason for each order.
- Allows users to adjust risk thresholds.

### 3. WhatsApp Confirmation Simulator
- Select an order and preview its confirmation message.
- Supports English and Telugu message previews.
- Simulates YES, NO, random reply, and no reply.
- Calculates the prepaid discount and final payable amount.

**Note:** This is a simulation. It does not send actual WhatsApp messages.

### 4. Financial Impact Dashboard
- Estimates the cost of an RTO.
- Calculates estimated RTO savings.
- Estimates potential loss from cancelling genuine orders.
- Displays the estimated net financial impact.

These are historical simulation estimates, not actual realised savings.

## Technology Stack

- Python
- Streamlit
- Pandas
- JSON
- Visual Studio Code

## Project Structure

```text
Oytra_COD_Project/
│
├── main.py
├── config.json
├── orders_sample.csv
└── README.md
```

## How to Run the Project

1. Install Python.
2. Open the project folder in Visual Studio Code.
3. Open the terminal.
4. Install the required packages:

```bash
.venv\Scripts\python.exe -m pip install streamlit pandas
```

5. Run the application:

```bash
.venv\Scripts\python.exe -m streamlit run main.py
```

6. Upload the CSV dataset in the application.

## Configuration

The `config.json` file stores configurable decision thresholds, including:

- High-risk previous RTO count
- Medium-risk previous RTO count
- High-value order threshold
- WhatsApp confirmation timeout
- Prepaid discount percentage

## Limitations

- WhatsApp responses are simulated; no real messages are sent.
- Financial results are estimates based on the assignment assumptions.
- The current decision engine uses rule-based classification. It does not have a connected LLM API.

## Project Objective

The objective is to reduce COD-related Return to Origin (RTO) losses while balancing operational costs and genuine customer orders.