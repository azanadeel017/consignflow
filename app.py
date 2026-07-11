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

# Custom CSS for rich aesthetics, emerald/slate color scheme, and clean typography
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
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
        transition: transform 0.2s ease-in-out, border-color 0.2s ease-in-out;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: #10b981; /* Emerald green highlight on hover */
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
        font-size: 28px;
        font-weight: 700;
    }
    
    .title-container {
        padding: 15px 0px 25px 0px;
        border-bottom: 1px solid #334155;
        margin-bottom: 30px;
    }
    .title-main {
        font-size: 40px;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 8px;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #f8fafc 0%, #10b981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .title-sub {
        font-size: 16px;
        color: #94a3b8;
    }
    
    .tab-header {
        font-size: 24px;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 20px;
        letter-spacing: -0.01em;
    }
    </style>
""", unsafe_allow_html=True)

# App Title & Description
st.markdown("""
    <div class="title-container">
        <div class="title-main">ConsignFlow Enterprise Portal</div>
        <div class="title-sub">Automated multi-platform transaction auditing, consignor split logic, and settlement BI.</div>
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
    try:
        stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
        data = load_and_parse_sales(stringio)
        st.sidebar.success("Successfully uploaded & parsed sales sheet!")
    except Exception as e:
        st.sidebar.error(f"Error parsing file: {e}")
        data = load_and_parse_sales(default_csv_path)
else:
    data = load_and_parse_sales(default_csv_path)

totals = data["totals"]
items_raw = data["items"]
platforms_raw = data["platforms"]

# -----------------------------------------------------
# DYNAMIC SPLIT CALCULATIONS & CONSIGNOR MATCHING
# -----------------------------------------------------
total_store_revenue = 0.0
total_consignor_payout = 0.0
items_processed = []
consignors_list = set()

for item in items_raw:
    title = item["item_title"]
    net_sale = item["net_payout"]
    
    # Extract Consignor prefix dynamically (first word of the title, e.g. "M1")
    words = title.split()
    consignor_name = words[0].upper() if words else "UNKNOWN"
    consignors_list.add(consignor_name)
    
    # Seller Payout = Net Payout * Consignor Split %
    consignor_payout = round(net_sale * (consignor_split / 100.0), 2)
    # Store Payout = Net Payout * Store Fee %
    store_revenue = round(net_sale - consignor_payout, 2)
    
    # Track totals
    total_store_revenue += store_revenue
    total_consignor_payout += consignor_payout
    
    items_processed.append({
        "Consignor": consignor_name,
        "Item Title": title,
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
unique_consignors = sorted(list(consignors_list))

# Convert to DataFrame
df_all = pd.DataFrame(items_processed) if items_processed else pd.DataFrame()

# -----------------------------------------------------
# TABBED NAVIGATION REDESIGN
# -----------------------------------------------------
tab1, tab2 = st.tabs(["📊 Store Analytics", "👤 Consignor Payouts"])

# ==========================================
# TAB 1: STORE ANALYTICS
# ==========================================
with tab1:
    st.markdown('<div class="tab-header">Executive Performance Indicators</div>', unsafe_allow_html=True)
    
    # KPI Grid
    kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)
    
    with kpi_col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Items Sold</div>
                <div class="metric-value" style="color: #a78bfa;">{totals['count']}</div>
            </div>
        """, unsafe_allow_html=True)

    with kpi_col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Gross Sales</div>
                <div class="metric-value" style="color: #38bdf8;">${totals['gross']:,.2f}</div>
            </div>
        """, unsafe_allow_html=True)

    with kpi_col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Marketplace Fees</div>
                <div class="metric-value" style="color: #f43f5e;">${totals['fees']:,.2f}</div>
            </div>
        """, unsafe_allow_html=True)

    with kpi_col4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Store Revenue ({store_fee_pct}%)</div>
                <div class="metric-value" style="color: #fbbf24;">${total_store_revenue:,.2f}</div>
            </div>
        """, unsafe_allow_html=True)

    with kpi_col5:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Seller Payouts ({consignor_split}%)</div>
                <div class="metric-value" style="color: #10b981;">${total_consignor_payout:,.2f}</div>
            </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")
    
    st.markdown('<div class="tab-header">Marketplace Channel Performance</div>', unsafe_allow_html=True)
    
    if platforms_raw:
        plot_data = []
        for platform_name, stats in platforms_raw.items():
            plt_gross = stats["gross"]
            plt_net = stats["net"]
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
            st.markdown("**Sales Contribution by Channel (Gross vs Net Proceeds)**")
            st.bar_chart(
                df_plot,
                x="Platform",
                y=["Gross Sales ($)", "Net Proceeds ($)"],
                color=["#f43f5e", "#38bdf8"],
                use_container_width=True
            )

        with chart_col2:
            st.markdown("**Channel Fee Efficiency (%)**")
            st.bar_chart(
                df_plot,
                x="Platform",
                y="Efficiency (%)",
                color="#10b981",
                use_container_width=True
            )
    else:
        st.info("No platform analytics data available.")

# ==========================================
# TAB 2: CONSIGNOR PAYOUTS
# ==========================================
with tab2:
    st.markdown('<div class="tab-header">Master Settlement Ledger</div>', unsafe_allow_html=True)
    
    if not df_all.empty:
        # Group and aggregate data for the Master Table
        df_master = df_all.groupby("Consignor").agg(
            Items_Sold=("Item Title", "count"),
            Gross_Revenue=("Gross Price", "sum"),
            Marketplace_Fees=("Total Fees", "sum"),
            Store_Commission=("Store Share", "sum"),
            Net_Payout_Owed=("Seller Share", "sum")
        ).reset_index()

        # Rename columns for clean representation
        df_master_display = df_master.rename(columns={
            "Items_Sold": "Items Sold",
            "Gross_Revenue": "Gross Revenue ($)",
            "Marketplace_Fees": "Marketplace Fees ($)",
            "Store_Commission": "Store Commission ($)",
            "Net_Payout_Owed": "Net Payout Owed ($)"
        })

        # Display Master Settlement Table
        st.dataframe(
            df_master_display,
            use_container_width=True,
            hide_index=True
        )
        
        st.write("")
        st.markdown('<div class="tab-header" style="font-size: 20px;">Individual Payout Statement</div>', unsafe_allow_html=True)
        
        # Dropdown selection for Consignor (placed below the master table)
        selected_consignor = st.selectbox(
            "Select Consignor Account",
            options=unique_consignors,
            help="Select a consignor to audit their individual ledger, review invoice math, and export data."
        )
        
        # Filter data for selected consignor
        df_filtered = df_all[df_all["Consignor"] == selected_consignor]
        
        # Calculations for Selected Consignor
        c_items = len(df_filtered)
        c_gross = df_filtered["Gross Price"].sum()
        c_fees = df_filtered["Total Fees"].sum()
        c_payout = df_filtered["Seller Share"].sum()
        c_store_revenue = df_filtered["Store Share"].sum()

        # Layout cols: Invoice Statement Card (Left) vs. Export Action (Right)
        inv_col1, inv_col2 = st.columns([3, 2])
        
        with inv_col1:
            # Styled digital payout invoice card
            st.markdown(f"""
                <div style="background-color: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 25px; font-family: 'Inter', sans-serif; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);">
                    <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #475569; padding-bottom: 12px; margin-bottom: 15px;">
                        <span style="font-weight: 800; font-size: 16px; color: #f8fafc; letter-spacing: 0.05em; text-transform: uppercase;">Consignment Settlement Invoice</span>
                        <span style="font-weight: 700; font-size: 15px; color: #10b981; background-color: rgba(16, 185, 129, 0.1); padding: 4px 8px; border-radius: 6px;">CONSIGNOR: {selected_consignor}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <span style="color: #94a3b8; font-size: 14px;">Gross Sales ({c_items} items)</span>
                        <span style="color: #f8fafc; font-weight: 600; font-size: 15px;">+${c_gross:,.2f}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <span style="color: #94a3b8; font-size: 14px;">Marketplace Fees</span>
                        <span style="color: #f43f5e; font-weight: 600; font-size: 15px;">-${c_fees:,.2f}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 15px; border-bottom: 1px dashed #475569; padding-bottom: 15px;">
                        <span style="color: #94a3b8; font-size: 14px;">Store Commission ({store_fee_pct}%)</span>
                        <span style="color: #f43f5e; font-weight: 600; font-size: 15px;">-${c_store_revenue:,.2f}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 20px; font-weight: 800; padding-top: 5px;">
                        <span style="color: #f8fafc;">Total Disbursed to Seller</span>
                        <span style="color: #10b981;">${c_payout:,.2f}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        with inv_col2:
            st.markdown("### 💾 Export Center")
            st.markdown(f"Generate and download the detailed invoice ledger report for `{selected_consignor}`. The file contains transaction-level sales, fee structures, and profit split records.")
            
            # Format clean individual consignor table (excluding grouped prefix column)
            df_display = df_filtered.drop(columns=["Consignor"])
            df_display.columns = [
                "Item Title", "Platform", "Gross Sales ($)", "Marketplace Fees ($)", 
                "Net proceeds ($)", "Store Split ($)", "Seller Split ($)"
            ]
            
            # Generate in-memory CSV export buffer
            csv_buffer = io.StringIO()
            df_display.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue()
            
            st.download_button(
                label=f"📥 Download {selected_consignor} Payout Ledger (CSV)",
                data=csv_data,
                file_name=f"consignor_{selected_consignor}_payout_ledger.csv",
                mime="text/csv",
                use_container_width=True
            )
            
        st.write("")
        st.write("")
        
        # Display detailed transaction table below
        st.markdown(f"#### Itemized Audit Log: `{selected_consignor}`")
        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No transaction data available.")
