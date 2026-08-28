# --- Visualizations & Data Table ---
st.subheader("Inventory & Sales Trajectory")

# Convert data for Plotly charting
df_melted = df.melt(
    id_vars=["Week"], 
    value_vars=["Ending Inventory ($)", "Purchases ($)", "Weekly COGS ($)"],
    var_name="Metric", 
    value_name="Amount ($)"
)

fig = px.line(
    df_melted, 
    x="Week", 
    y="Amount ($)", 
    color="Metric",
    markers=True,
    title="Inventory & Sales Trajectory (2026 Calendar)"
)

# Enforce explicit array chronological ordering on X-axis
fig.update_xaxes(
    type='category', 
    tickangle=-45,
    categoryorder="array",
    categoryarray=df["Week"].tolist()
)
fig.update_layout(hovermode="x unified")

st.plotly_chart(fig, use_container_width=True)

st.subheader("Weekly Breakdown")
st.dataframe(df, use_container_width=True)