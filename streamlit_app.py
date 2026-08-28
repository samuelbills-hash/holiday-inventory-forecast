import streamlit as st
import pandas as pd

st.set_page_config(page_title="Holiday Retail Purchasing Forecast", layout="wide")

st.title("🎄 Holiday Retail Purchasing & Inventory Simulator")
st.markdown("Adjust the parameters on the sidebar to update weekly purchasing and inventory projections.")

# --- Sidebar Inputs ---
st.sidebar.header("Forecast Settings")
start_inv = st.sidebar.number_input("Starting Inventory ($)", value=40000, step=5000)
gross_margin = st.sidebar.slider("Gross Margin (%)", min_value=30, max_value=70, value=52) / 100
target_ending_inv = st.sidebar.number_input("Target Dec 31 Inventory Buffer ($)", value=0, step=2500)

# Monthly Retail Sales Inputs
st.sidebar.subheader("Monthly Retail Sales")
sep_sales = st.sidebar.number_input("September Sales ($)", value=20000)
oct_sales = st.sidebar.number_input("October Sales ($)", value=30000)
nov_sales = st.sidebar.number_input("November Sales ($)", value=60000)
dec_sales = st.sidebar.number_input("December Sales ($)", value=140000)

total_sales = sep_sales + oct_sales + nov_sales + dec_sales
cogs_rate = 1 - gross_margin
total_cogs = total_sales * cogs_rate
net_purchases_needed = max(0.0, total_cogs + target_ending_inv - start_inv)

# --- Key Metrics Summary ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Retail Sales", f"${total_sales:,.0f}")
col2.metric("Total COGS Needed", f"${total_cogs:,.0f}")
col3.metric("Starting Inventory", f"${start_inv:,.0f}")
col4.metric("Net Purchases Needed", f"${net_purchases_needed:,.0f}")

# --- Weekly Purchasing Allocation Logic ---
# 17 weeks total (Sep: 4 wks, Oct: 4 wks, Nov: 4 wks, Dec: 5 wks)
front_load_purchases = net_purchases_needed * 0.90  # 90% by mid-Nov (Weeks 1-10)
remaining_purchases = net_purchases_needed * 0.10   # 10% late Nov/Dec (Weeks 11-17)

weekly_data = []
curr_inv = start_inv

sales_by_week = [
    sep_sales/4]*4 + [oct_sales/4]*4 + [nov_sales/4]*4 + [dec_sales/5]*5

for w in range(1, 18):
    w_sales = sales_by_week[w-1]
    w_cogs = w_sales * cogs_rate
    
    # Purchasing Logic: Front-load 90% across W1-W10, remaining across W11-W15
    if w <= 8:
        w_pur = (front_load_purchases * 0.88) / 8  # Sept & Oct build
    elif w <= 10:
        w_pur = (front_load_purchases * 0.12) / 2  # Early Nov build
    elif w <= 15:
        w_pur = remaining_purchases / 5            # Late Nov / Dec top-ups
    else:
        w_pur = 0.0                                 # Year-end sell-through
        
    curr_inv = curr_inv + w_pur - w_cogs
    
    weekly_data.append({
        "Week": f"Week {w}",
        "Weekly Sales ($)": round(w_sales, 2),
        "Weekly COGS ($)": round(w_cogs, 2),
        "Purchases ($)": round(w_pur, 2),
        "Ending Inventory ($)": round(curr_inv, 2)
    })

df = pd.DataFrame(weekly_data)

# --- Visualizations & Data Table ---
st.subheader("Inventory & Sales Trajectory")
st.line_chart(df.set_index("Week")[["Purchases ($)", "Ending Inventory ($)", "Weekly COGS ($)"]])

st.subheader("Weekly Breakdown")
st.dataframe(df, use_container_width=True)