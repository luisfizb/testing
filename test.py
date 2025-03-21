import streamlit as st
import pandas as pd
import altair as alt

# Sample DataFrame (replace with your own data or CSV)
data = {
    "Name": ["Alice", "Bob", "Charlie", "David", "Eve"],
    "Department": ["HR", "IT", "IT", "Finance", "HR"],
    "Age": [25, 30, 35, 40, 28],
    "Salary": [50000, 60000, 70000, 80000, 52000]
}
df = pd.DataFrame(data)

st.title("Interactive Table and Horizontal Bar Chart with Filters")

# Filters
with st.expander("Filter Options"):
    name_filter = st.text_input("Filter by Name (contains)")
    dept_options = df["Department"].unique().tolist()
    dept_filter = st.selectbox("Filter by Department", ["All"] + dept_options)

    age_min, age_max = st.slider(
        "Filter by Age Range",
        int(df["Age"].min()), int(df["Age"].max()),
        (int(df["Age"].min()), int(df["Age"].max()))
    )

# Apply filters
filtered_df = df.copy()

if name_filter:
    filtered_df = filtered_df[filtered_df["Name"].str.contains(name_filter, case=False)]

if dept_filter != "All":
    filtered_df = filtered_df[filtered_df["Department"] == dept_filter]

filtered_df = filtered_df[(filtered_df["Age"] >= age_min) & (filtered_df["Age"] <= age_max)]

# Display filtered table
st.subheader("Filtered Table")
st.dataframe(filtered_df, use_container_width=True)

# Horizontal Bar Chart: Total Salary by Department
st.subheader("Total Salary by Department (Horizontal Bar Chart)")

if not filtered_df.empty:
    chart_data = filtered_df.groupby("Department", as_index=False)["Salary"].sum()

    bar_chart = alt.Chart(chart_data).mark_bar().encode(
        y=alt.Y("Department", sort="-x"),
        x="Salary",
        tooltip=["Department", "Salary"]
    ).properties(height=400)

    st.altair_chart(bar_chart, use_container_width=True)
else:
    st.info("No data to display in chart.")
