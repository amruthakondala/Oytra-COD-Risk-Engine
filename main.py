
import streamlit as st
import pandas as pd
import json
import re

st.set_page_config(
    page_title="Oytra COD Decision Engine",
    layout="wide"
)

st.title("Oytra COD Decision Engine")
st.write("COD Order Risk Analysis and Decision System")

# Load configuration
with open("config.json", "r") as file:
    config = json.load(file)

# CSV Upload
uploaded_file = st.file_uploader(
    "Upload COD Orders Dataset",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    required_columns = [
        "order_id", "order_datetime", "customer_name",
        "address", "city", "order_value",
        "customer_prior_orders", "customer_prior_rto",
        "payment_method", "final_status"
    ]

    missing = [c for c in required_columns if c not in df.columns]

    if missing:
        st.error("Missing columns: " + ", ".join(missing))
        st.stop()

    # Standardize data
    df["final_status"] = (
        df["final_status"].astype(str).str.strip().str.upper()
    )

    df["payment_method"] = (
        df["payment_method"].astype(str).str.strip().str.upper()
    )

    df["order_datetime"] = pd.to_datetime(
        df["order_datetime"], errors="coerce"
    )

    for column in [
        "customer_prior_orders",
        "customer_prior_rto",
        "order_value"
    ]:
        df[column] = pd.to_numeric(
            df[column], errors="coerce"
        ).fillna(0)

    # Normalize status variations
    df["final_status"] = df["final_status"].replace({
        "RETURNED": "RTO",
        "RETURN TO ORIGIN": "RTO"
    })

    # Duplicate check
    duplicate_count = int(df["order_id"].duplicated().sum())

    if duplicate_count > 0:
        st.warning(
            f"{duplicate_count} duplicate order IDs found. "
            "Keeping the latest record for each order."
        )

        df = df.sort_values("order_datetime")
        df = df.drop_duplicates(
            subset="order_id", keep="last"
        ).copy()

    st.success("Dataset uploaded and processed successfully!")

    # 1. Dataset Overview
    st.header("1. Dataset Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Unique Orders", len(df))
    col2.metric("Total Columns", len(df.columns))
    col3.metric("Duplicate IDs Found", duplicate_count)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # 2. Order Status Analysis
    st.header("2. Order Status Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Order Status")
        st.write(df["final_status"].value_counts())

    with col2:
        st.subheader("Payment Methods")
        st.write(df["payment_method"].value_counts())

    # 3. RTO Analysis
    st.header("3. RTO Analysis")

    valid_orders = df[
        df["final_status"].isin(["DELIVERED", "RTO"])
    ]

    total_valid = len(valid_orders)
    rto_orders = int(
        (valid_orders["final_status"] == "RTO").sum()
    )

    if total_valid > 0:
        rto_rate = rto_orders / total_valid * 100

        col1, col2, col3 = st.columns(3)
        col1.metric("Valid Orders", total_valid)
        col2.metric("RTO Orders", rto_orders)
        col3.metric("RTO Rate", f"{rto_rate:.2f}%")

    # 4. Decision Engine Settings
    st.header("4. Decision Engine Settings")

    col1, col2 = st.columns(2)

    with col1:
        high_rto = st.number_input(
            "High Risk Previous RTO Count",
            min_value=1,
            value=int(config["high_risk_prior_rto"])
        )

        medium_rto = st.number_input(
            "Medium Risk Previous RTO Count",
            min_value=0,
            value=int(config["medium_risk_prior_rto"])
        )

    with col2:
        high_value = st.number_input(
            "High Value Order Amount (₹)",
            min_value=1,
            value=int(config["high_risk_order_value"])
        )

        discount = st.number_input(
            "Prepaid Discount (%)",
            min_value=0,
            max_value=100,
            value=int(config["prepaid_discount_percent"])
        )

    # Basic text-risk checks
    def check_text_risk(row):
        name = str(row["customer_name"]).strip()
        address = str(row["address"]).strip()

        reasons = []

        if len(name) < 3 or re.search(r"\d", name):
            reasons.append("Unusual or incomplete customer name")

        if len(address) < 12:
            reasons.append("Address may be incomplete")

        if address.lower() in ["nan", "none", "unknown", "na", ""]:
            reasons.append("Address is missing")

        return reasons

    df["text_warnings"] = df.apply(check_text_risk, axis=1)

    # 5. COD Decision Engine
    st.header("5. COD Order Decisions")

    def decide_order(row):
        prior_rto = row["customer_prior_rto"]
        prior_orders = row["customer_prior_orders"]
        order_value = row["order_value"]
        warnings = row["text_warnings"]

        if prior_rto >= high_rto:
            return pd.Series([
                "Hold-cancel",
                "Multiple previous RTOs"
            ])

        elif warnings:
            return pd.Series([
                "Ship after WhatsApp confirmation",
                "; ".join(warnings)
            ])

        elif medium_rto > 0 and prior_rto >= medium_rto:
            return pd.Series([
                "Ship after WhatsApp confirmation",
                "Previous RTO found"
            ])

        elif prior_orders == 0:
            return pd.Series([
                "Ship after WhatsApp confirmation",
                "First-time customer"
            ])

        elif order_value >= high_value:
            return pd.Series([
                "Nudge to prepaid",
                "High-value order"
            ])

        else:
            return pd.Series([
                "Ship as-is",
                "Returning customer with low RTO history"
            ])

    df[["decision", "decision_reason"]] = df.apply(
        decide_order, axis=1
    )

    st.subheader("Decision Summary")

    decision_order = [
        "Ship as-is",
        "Ship after WhatsApp confirmation",
        "Nudge to prepaid",
        "Hold-cancel"
    ]

    decision_counts = (
        df["decision"]
        .value_counts()
        .reindex(decision_order, fill_value=0)
    )

    st.bar_chart(decision_counts)

    cols = st.columns(4)
    for i, decision in enumerate(decision_order):
        cols[i].metric(decision, int(decision_counts[decision]))

    st.subheader("Order Decisions Preview")

    display_columns = [
        "order_id", "customer_name", "city",
        "order_value", "customer_prior_orders",
        "customer_prior_rto", "decision",
        "decision_reason"
    ]

    st.dataframe(df[display_columns].head(50))

    st.download_button(
        "Download Decisions CSV",
        df.to_csv(index=False).encode("utf-8"),
        "oytra_order_decisions.csv",
        "text/csv"
    )

    # Latest date summary
    st.subheader("Latest Order Date Summary")

    if df["order_datetime"].notna().any():
        latest_date = df["order_datetime"].max().date()

        latest_orders = df[
            df["order_datetime"].dt.date == latest_date
        ]

        st.write(
            f"Showing orders from the latest date in the dataset: "
            f"{latest_date}"
        )

        latest_counts = (
            latest_orders["decision"]
            .value_counts()
            .reindex(decision_order, fill_value=0)
        )

        cols = st.columns(4)
        for i, decision in enumerate(decision_order):
            cols[i].metric(
                decision, int(latest_counts[decision])
            )

    else:
        st.warning("Order dates could not be identified.")

    # Text warning review
    st.subheader("Address and Name Review")

    text_review = df[df["text_warnings"].map(bool)]

    if len(text_review) > 0:
        st.write(
            "These orders have basic text-quality warnings "
            "and may need manual review."
        )
        st.dataframe(
            text_review[
                ["order_id", "customer_name", "address", "text_warnings"]
            ]
        )
    else:
        st.success("No basic text-quality warnings found.")

    st.caption(
        "Text warnings use simple rule-based checks. "
        "They are not LLM analysis or proof of a fake customer."
    )

    # 6. WhatsApp Confirmation Simulator
    st.header("6. WhatsApp Confirmation Simulator")

    st.write(
        "Select an order and simulate the customer's response."
    )

    order_ids = df["order_id"].astype(str).tolist()

    selected_order = st.selectbox(
        "Select Order ID", order_ids
    )

    order = df[
        df["order_id"].astype(str) == selected_order
    ].iloc[0]

    order_amount = float(order["order_value"])

    language = st.selectbox(
        "Select Message Language",
        ["English", "Telugu"]
    )

    if language == "English":
        message = (
            f"Hello {order['customer_name']}, "
            f"we received your COD order worth ₹{order_amount:.2f}. "
            "Please confirm by replying YES or NO."
        )
    else:
        message = (
            f"Namaste {order['customer_name']}, "
            f"mee ₹{order_amount:.2f} COD order receive ayyindhi. "
            "Confirm cheyyadaniki YES or NO ani reply ivvandi."
        )

    st.subheader("WhatsApp Message Preview")
    st.info(message)

    st.write("Message Timing: Immediately after order placement")

    response = st.radio(
        "Simulate Customer Response",
        ["YES", "NO", "Random Reply", "No Reply"]
    )

    if st.button("Simulate WhatsApp Response"):

        if response == "YES":
            st.success(
                "Customer confirmed the order. "
                "Proceed with order processing."
            )

        elif response == "NO":
            st.warning(
                "Customer rejected the order. "
                "Hold the order for manual review."
            )

        elif response == "Random Reply":
            st.warning(
                "Unclear response received. "
                "Send for manual review."
            )

        else:
            st.error(
                "No reply received within 24 hours. "
                "Keep the order on hold for manual review."
            )

    # Prepaid Discount Calculator
    st.subheader("Prepaid Discount Calculator")

    discount_amount = order_amount * discount / 100
    prepaid_price = order_amount - discount_amount

    col1, col2, col3 = st.columns(3)
    col1.metric("Original Order Value", f"₹{order_amount:.2f}")
    col2.metric("Prepaid Discount", f"₹{discount_amount:.2f}")
    col3.metric("Prepaid Amount", f"₹{prepaid_price:.2f}")

    # 7. Financial Impact Dashboard
    st.header("7. Financial Impact Dashboard")

    st.write("Assignment-based cost assumptions")

    forward_shipping = 65
    return_shipping = 65
    packaging_cost = 25
    damage_rate = 0.08
    product_cost = 180
    gross_margin = 0.62

    rto_cost = (
        forward_shipping
        + return_shipping
        + packaging_cost
        + (damage_rate * product_cost)
    )

    st.write(f"Expected cost per RTO: ₹{rto_cost:.2f}")

    cancelled_orders = df[
        df["decision"] == "Hold-cancel"
    ]

    historical_rto = cancelled_orders[
        cancelled_orders["final_status"] == "RTO"
    ]

    historical_delivered = cancelled_orders[
        cancelled_orders["final_status"] == "DELIVERED"
    ]

    estimated_rto_savings = len(historical_rto) * rto_cost

    estimated_genuine_loss = (
        historical_delivered["order_value"].sum()
        * gross_margin
    )

    estimated_net_impact = (
        estimated_rto_savings - estimated_genuine_loss
    )

    st.subheader("Retrospective Financial Simulation")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Potential RTO Cost Avoidance",
        f"₹{estimated_rto_savings:,.2f}"
    )

    col2.metric(
        "Potential Genuine Order Margin Loss",
        f"₹{estimated_genuine_loss:,.2f}"
    )

    col3.metric(
        "Estimated Net Impact",
        f"₹{estimated_net_impact:,.2f}"
    )

    st.subheader("Cancellation Analysis")

    col1, col2 = st.columns(2)

    col1.metric(
        "Historical RTO Orders in Hold-cancel",
        len(historical_rto)
    )

    col2.metric(
        "Historical Delivered Orders in Hold-cancel",
        len(historical_delivered)
    )

    st.caption(
        "This is a retrospective estimate using historical outcomes. "
        "It does not prove that these RTOs would have been prevented "
        "or that genuine orders would actually have been cancelled."
    )

    st.info(
        "LLM integration is not enabled in this version. "
        "Ambiguous text is flagged using basic rule-based checks."
    )

else:
    st.info("Please upload your COD orders CSV file to begin.")
