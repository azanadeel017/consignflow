import streamlit as st
import pandas as pd
import os

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
        padding: 24px;
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
        font-size: 14px;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 8px;
        letter-spacing: 0.05em;
    }
    .metric-value {
        font-size: 32px;
        color: #38bdf8;
        font-weight: 700;
    }
    .title-container {
        padding: 10px 0px 25px 0px;
        border-bottom: 1px solid #334155;
        margin-bottom: 25px;
    }
    .title-main {
        font-size: 40px;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 8px;
        letter-spacing: -0.02em;
    }
    .title-sub {
        font-size: 18px;
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

# Resolve file path to data
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "mock_sales.csv")

# Load data from the backend Strategy engine
data = load_and_parse_sales(csv_path)
totals = data["totals"]
items_raw = data["items"]
platforms_raw = data["platforms"]

# Create DataFrame for matched transactions
if items_raw:
    df_items = pd.DataFrame(items_raw)
    # Rename columns for clean presentation
    df_items.columns = [
        "Item Title", "Platform", "Gross Price ($)", 
        "Commission ($)", "Tx Fee ($)", "Flat Fee ($)", 
        "Total Fees ($)", "Net Payout ($)"
    ]
else:
    df_items = pd.DataFrame()

# -----------------------------------------------------
# EXECUTIVE KPI CARDS
# -----------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Volume</div>
            <div class="metric-value" style="color: #a78bfa;">{totals['count']} Items</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Gross Revenue</div>
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
            <div class="metric-label">Net Profit Margin</div>
            <div class="metric-value" style="color: #34d399;">{totals['margin']:.2f}%</div>
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
            "Net Profit ($)": plt_net,
            "Efficiency (%)": round(efficiency, 2)
        })
    df_plot = pd.DataFrame(plot_data)

    chart_col1, chart_col2 = st.columns([2, 1])

    with chart_col1:
        st.markdown("**Sales Breakdown by Platform (Gross vs Net)**")
        # Native Streamlit bar chart comparing Gross vs Net
        st.bar_chart(
            df_plot,
            x="Platform",
            y=["Gross Sales ($)", "Net Profit ($)"],
            color=["#f43f5e", "#38bdf8"],
            use_container_width=True
        )

    with chart_col2:
        st.markdown("**Platform Payout Efficiency (%)**")
        # Show margins in a bar chart
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
    st.sidebar.header("🔍 Filter Ledger")
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
