import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------
# PAGE SETUP
# ---------------------------------------------
st.set_page_config(page_title="Employee Analytics Dashboard", layout="wide")

st.title("📊 Employee Profiling & Analytics Dashboard")

st.write("This dashboard provides insights into employee performance, satisfaction, stress levels, and attrition risk.")

# ---------------------------------------------
# DATA UPLOAD
# ---------------------------------------------
uploaded = st.file_uploader("Upload final_dataset.csv", type=["csv"])

df = None # Initialize df to None

if uploaded is None:
    st.info("Please upload final_dataset.csv generated from your preprocessing pipeline.")
    st.stop() # Use st.stop() to halt execution in Streamlit when no file is uploaded.
else:
    df = pd.read_csv(uploaded)

# Only proceed with dashboard generation if df was successfully loaded
if df is not None:
    # ---------------------------------------------
    # SIDEBAR FILTERS
    # ---------------------------------------------
    st.sidebar.header("🔎 Filters")

    dept_filter = st.sidebar.selectbox("Select Department", ["All"] + sorted(df["Department"].unique()))
    gender_filter = st.sidebar.selectbox("Select Gender", ["All"] + sorted(df["Gender"].unique()))

    df_filtered = df.copy()

    if dept_filter != "All":
        df_filtered = df_filtered[df_filtered["Department"] == dept_filter]

    if gender_filter != "All":
        df_filtered = df_filtered[df_filtered["Gender"] == gender_filter]

    # ---------------------------------------------
    # KPI CARDS
    # ---------------------------------------------
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Employees", df_filtered.shape[0])
    col2.metric("Avg Satisfaction", f"{df_filtered['Satisfaction'].mean():.2f}")
    col3.metric("Avg Performance", f"{df_filtered['PerformanceScore'].mean():.2f}")
    col4.metric("Profiles", df_filtered['LPA_Profile'].nunique())

    st.markdown("---")

    # ---------------------------------------------
    # VISUAL 1: LPA PROFILE DISTRIBUTION
    # ---------------------------------------------
    st.subheader("1️⃣ LPA Profile Distribution")

    fig1 = px.bar(
        df_filtered["LPA_Profile"].value_counts().reset_index(),
        x="index", y="LPA_Profile",
        color="index",
        labels={"index": "LPA Profile", "LPA_Profile": "Count"},
        title="Employees Per Profile"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # ---------------------------------------------
    # VISUAL 2: Department Count
    # ---------------------------------------------
    st.subheader("2️⃣ Department Distribution")

    fig2 = px.pie(
        df_filtered,
        names="Department",
        title="Employee Department Share"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # ---------------------------------------------
    # VISUAL 3: Performance vs Satisfaction
    # ---------------------------------------------
    st.subheader("3️⃣ Performance vs Satisfaction")

    fig3 = px.scatter(
        df_filtered,
        x="PerformanceScore",
        y="Satisfaction",
        color="LPA_Profile",
        size="Engagement",
        hover_data=["EmployeeID", "Department"],
        title="Performance vs Satisfaction Colored by Profile"
    )
    st.plotly_chart(fig3, use_container_width=True)

    # ---------------------------------------------
    # VISUAL 4: Stress Distribution
    # ---------------------------------------------
    st.subheader("4️⃣ Stress Level Distribution")

    fig4 = px.histogram(
        df_filtered,
        x="Stress",
        nbins=20,
        color="Gender",
        title="Stress Distribution"
    )
    st.plotly_chart(fig4, use_container_width=True)

    # ---------------------------------------------
    # VISUAL 5: Work-Life Balance Boxplot
    # ---------------------------------------------
    st.subheader("5️⃣ Work-Life Balance by Department")

    fig5 = px.box(
        df_filtered,
        x="Department",
        y="WorkLifeBalance",
        color="Department",
        title="Work-Life Balance Variation Across Departments"
    )
    st.plotly_chart(fig5, use_container_width=True)

    # ---------------------------------------------
    # VISUAL 6: Correlation Heatmap
    # ---------------------------------------------
    st.subheader("6️⃣ Correlation Heatmap (Numeric Features)")

    num_cols = [
        "Age","TenureMonths","PerformanceScore","Satisfaction","Engagement",
        "Motivation","Stress","WorkLifeBalance","OvertimeHours",
        "TrainingHoursLastYear","AbsenteeismDays","PeerRating",
        "ManagerRating","ProjectLoad","LPA_Profile"
    ]

    corr = df_filtered[num_cols].corr()

    fig6 = px.imshow(
        corr,
        text_auto=True,
        title="Correlation Heatmap"
    )
    st.plotly_chart(fig6, use_container_width=True)

    # ---------------------------------------------
    # VISUAL 7: Attrition by Profile
    # ---------------------------------------------
    if "Attrition" in df_filtered.columns:
        st.subheader("7️⃣ Attrition Rate by LPA Profile")

        attr_data = df_filtered.groupby("LPA_Profile")["Attrition"].mean().reset_index()
        attr_data["Attrition"] = attr_data["Attrition"] * 100

        fig7 = px.bar(
            attr_data,
            x="LPA_Profile",
            y="Attrition",
            color="LPA_Profile",
            title="Attrition % by Profile",
            labels={"Attrition": "Attrition (%)"}
        )

        st.plotly_chart(fig7, use_container_width=True)
    else:
        st.warning("Attrition column not found in dataset.")

    st.success("Dashboard Loaded Successfully!")
