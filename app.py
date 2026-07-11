import streamlit as st
import pandas as pd
import os
import io

# Import our backend parser engine
from parser import load_and_parse_sales

# Set page configuration for a premium dashboard feel
st.set_page_config(
    page_title="ConsignFlow Financial Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for rich aesthetics and clean typography
st.markdown("""
    <style>
    .main {
        background-color: #0f172a;
        color: #f8fafc;
    }
    .metric-card {
        background-color: #1e293b;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #334155;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        transition: transform 0.2s ease-in-out;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: #475569;
    }
    .metric-label {
        font-size: 13px;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 8px;
        letter-spacing: 0.05em;
    }
    .metric-value {
        font-size: 26px;
        font-weight: 700;
    }
    .title-container {
        padding: 10px 0px 25px 0px;
        border-bottom: 1px solid #334155;
        margin-bottom: 25px;
    }
    .title-main {
        font-size: 36px;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 8px;
        letter-spacing: -0.02em;
    }
    .title-sub {
        font-size: 16px;
        color: #94a3b8;
    }
    </style>
""", unsafe_allow_html=True)

# App Title & Description
st.markdown("""
    <div class="title-container">
        <div class="title-main">📊 ConsignFlow Executive Dashboard</div>
        <div class="title-sub">Real-time marketplace transaction auditing and business intelligence analytics.</div>
    </div>
""", unsafe_allow_html=True)

# -----------------------------------------------------
# SIDEBAR CONTROLS
# -----------------------------------------------------
st.sidebar.header("⚙️ Configuration")

# Slider control for Consignor Split (Default 80% to consignor, 20% store fee)
consignor_split = st.sidebar.slider(
    "Consignor Split % (Payout)",
    min_value=0,
    max_value=100,
    value=80,
    step=5,
    help="Percentage of Net Sale proceeds paid to the seller. The remainder is kept by the store."
)

store_fee_pct = 100 - consignor_split
st.sidebar.markdown(f"**Store Commission Split:** `{store_fee_pct}%`")

# File Uploader
st.sidebar.subheader("📥 Upload Sales Ledger")
uploaded_file = st.sidebar.file_uploader(
    "Upload a CSV file containing sales", 
    type=["csv"],
    help="Upload your marketplace sales sheet with 'Item Title', 'Sale Price', and 'Platform' columns."
)

# -----------------------------------------------------
# DATA LOADING & RE-PROCESSING
# -----------------------------------------------------
# Resolve fallback file path to mock data if no upload
script_dir = os.path.dirname(os.path.abspath(__file__))
default_csv_path = os.path.join(script_dir, "mock_sales.csv")

if uploaded_file is not None:
    # Read the uploaded CSV bytes, decode to UTF-8, and wrap in StringIO for parser
    try:
        stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
        data = load_and_parse_sales(stringio)
        st.sidebar.success("Successfully uploaded & parsed sales sheet!")
    except Exception as e:
        st.sidebar.error(f"Error parsing file: {e}")
        # Fall back to default template
        data = load_and_parse_sales(default_csv_path)
else:
    # Use default mock data
    data = load_and_parse_sales(default_csv_path)

# Extract core dataset components
totals = data["totals"]
items_raw = data["items"]
platforms_raw = data["platforms"]

# -----------------------------------------------------
# DYNAMIC SPLIT CALCULATIONS
# -----------------------------------------------------
# Re-evaluate payouts and store splits dynamically based on the slider value
total_store_revenue = 0.0
total_consignor_payout = 0.0
items_with_split = []

for item in items_raw:
    net_sale = item["net_payout"]
    # Seller (Consignor) Payout = Net Payout * Consignor Split %
    consignor_payout = round(net_sale * (consignor_split / 100.0), 2)
    # Store Payout = Net Payout * Store Fee %
    store_revenue = round(net_sale - consignor_payout, 2)
    
    # Track totals
    total_store_revenue += store_revenue
    total_consignor_payout += consignor_payout
    
    # Store split-calculated record
    items_with_split.append({
        "Item Title": item["item_title"],
        "Platform": item["platform"],
        "Gross Price": item["gross_price"],
        "Total Fees": item["total_fees"],
        "Net Sale": net_sale,
        "Store Share": store_revenue,
        "Seller Share": consignor_payout
    })

# Format split totals
total_store_revenue = round(total_store_revenue, 2)
total_consignor_payout = round(total_consignor_payout, 2)

# Create DataFrame
if items_with_split:
    df_items = pd.DataFrame(items_with_split)
else:
    df_items = pd.DataFrame()

# -----------------------------------------------------
# EXECUTIVE KPI CARDS
# -----------------------------------------------------
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Processed Items</div>
            <div class="metric-value" style="color: #a78bfa;">{totals['count']} Items</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Gross Sales</div>
            <div class="metric-value" style="color: #38bdf8;">${totals['gross']:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Marketplace Fees</div>
            <div class="metric-value" style="color: #f43f5e;">${totals['fees']:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Store Revenue ({store_fee_pct}%)</div>
            <div class="metric-value" style="color: #fbbf24;">${total_store_revenue:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Seller Payouts ({consignor_split}%)</div>
            <div class="metric-value" style="color: #34d399;">${total_consignor_payout:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# -----------------------------------------------------
# CHARTS & VISUALIZATIONS
# -----------------------------------------------------
st.subheader("📈 Channel Efficiency Analysis")

if platforms_raw:
    # Prepare data for plotting platform efficiency
    plot_data = []
    for platform_name, stats in platforms_raw.items():
        plt_gross = stats["gross"]
        plt_net = stats["net"]
        # Calculate platform efficiency percentage
        efficiency = (plt_net / plt_gross * 100) if plt_gross > 0 else 0.0
        plot_data.append({
            "Platform": platform_name,
            "Gross Sales ($)": plt_gross,
            "Total Fees ($)": stats["fees"],
            "Net Proceeds ($)": plt_net,
            "Efficiency (%)": round(efficiency, 2)
        })
    df_plot = pd.DataFrame(plot_data)

    chart_col1, chart_col2 = st.columns([2, 1])

    with chart_col1:
        st.markdown("**Sales Breakdown by Platform (Gross vs Net Proceeds)**")
        st.bar_chart(
            df_plot,
            x="Platform",
            y=["Gross Sales ($)", "Net Proceeds ($)"],
            color=["#f43f5e", "#38bdf8"],
            use_container_width=True
        )

    with chart_col2:
        st.markdown("**Platform Payout Efficiency (%)**")
        st.bar_chart(
            df_plot,
            x="Platform",
            y="Efficiency (%)",
            color="#34d399",
            use_container_width=True
        )
else:
    st.info("No platform analytics data available.")

st.write("")

# -----------------------------------------------------
# TRANSACTION LEDGER TABLE WITH SEARCH
# -----------------------------------------------------
st.subheader("📋 Transaction Ledger")

if not df_items.empty:
    # Sidebar Filters
    st.sidebar.subheader("🔍 Filter Ledger")
    search_query = st.sidebar.text_input("Search Item Title", "")
    
    selected_platform = st.sidebar.multiselect(
        "Filter by Platform",
        options=df_items["Platform"].unique(),
        default=df_items["Platform"].unique()
    )

    # Apply search & platform filters
    filtered_df = df_items[
        df_items["Item Title"].str.contains(search_query, case=False, na=False) &
        df_items["Platform"].isin(selected_platform)
    ]

    # Display clean dataframe
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No transactions found in the mock ledger.")
