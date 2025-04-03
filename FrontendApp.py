import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Streamlit page configuration
st.set_page_config(page_title="Credit Card Insights Dashboard", page_icon="💳", layout="wide")

# Custom CSS for Advanced Dark UI
st.markdown("""
    <style>
        body {
            background-color: #0e1117;
            color: #ffffff;
        }
        .reportview-container .main .block-container {
            padding: 2rem 2rem 2rem 2rem;
            background-color: #0e1117;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #ffffff;
        }
        .stButton>button {
            background-color: #1f77b4;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            border: none;
        }
        .stDataFrame, .stTable, .stTextInput>div>div>input {
            background-color: #20232a;
            color: #ffffff;
            border-radius: 8px;
        }
        .stSlider>div>div>div>input {
            background-color: #20232a;
            color: #ffffff;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("""
    <h1 style='text-align: center; font-size: 3rem;'>💳 Credit Card Launch Dashboard</h1>
    <hr style='border: 2px solid #444;'>
""", unsafe_allow_html=True)


# Load datasets
@st.cache_data
def load_data():
    customers = pd.read_csv("customers.csv")
    transactions = pd.read_csv("transactions.csv")
    credit_profiles = pd.read_csv("credit_profiles.csv")
    avg_transactions = pd.read_csv("avg_transactions_after_campaign.csv")
    return customers, transactions, credit_profiles, avg_transactions


customers, transactions, credit_profiles, avg_transactions = load_data()

# Tabs for navigation
tabs = st.tabs(
    ["📊 Overview", "👤 Demographics Analysis", "💰 Transaction Insights", "💳 Credit Profiles", "📈 Final Recommendation"])

# Overview
with tabs[0]:
    st.subheader(" Project Summary")
    st.markdown("""
    This dashboard provides data-driven insights derived from over 50,000 customer records to help identify the most suitable target audience for a **new credit card launch**.

    **Data Sources:**
    - Customer Demographics
    - Transactional Behaviour
    - Credit Profiles
    - Post-campaign Purchase Patterns
    """)
    st.markdown("""---""")
    st.write("### Sample Data Preview:")
    st.dataframe(customers.head(), use_container_width=True)

# Demographics Analysis
with tabs[1]:
    st.subheader("👤 Customer Demographics Insights")
    age_plot = sns.histplot(customers['age'], kde=True, bins=30, color='skyblue')
    st.pyplot(age_plot.figure)

    gender_dist = customers['gender'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(gender_dist, labels=gender_dist.index, autopct='%1.1f%%', startangle=90, colors=['#FF69B4', '#87CEEB'])
    ax.axis('equal')
    st.pyplot(fig)

# Transaction Insights
with tabs[2]:
    st.subheader("💰 Transactional Behaviour")
    top_platforms = transactions['platform'].value_counts().head(10)
    st.bar_chart(top_platforms)

    transactions['tran_date'] = pd.to_datetime(transactions['tran_date'])
    tran_by_month = transactions.groupby(transactions['tran_date'].dt.to_period("M")).size()
    st.line_chart(tran_by_month)

# Credit Profiles
with tabs[3]:
    st.subheader("💳 Credit Profiles Overview")
    fig, ax = plt.subplots()
    sns.boxplot(data=credit_profiles, x='credit_score', color='#4DB6AC', ax=ax)
    st.pyplot(fig)

    correlation_matrix = credit_profiles.corr(numeric_only=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

# Final Recommendation
with tabs[4]:
    st.subheader("📈 Credit Card Launch Recommendation")

    age_group = pd.cut(customers['age'], bins=[18, 25, 35, 45, 60], labels=["18-25", "26-35", "36-45", "46-60"])
    age_counts = age_group.value_counts().sort_index()
    st.bar_chart(age_counts)

    avg_income_by_age = customers.groupby(age_group)['annual_income'].mean()
    st.line_chart(avg_income_by_age)

    st.markdown("""
    #### Recommendation Summary:
    - **Target Age Group:** 26-35 years – highest activity and healthy credit scores.
    - **Preferred Card Type:** Lifestyle & Cashback Rewards Card.
    - **Additional Benefits:** Online shopping rewards, flexible EMI plans, low annual fee.
    """)

# --- Section 7: Interactive Filters ---
with tabs[0]:  # You can keep it under the overview tab or a separate one
    st.header("🔎 Interactive Customer Filter")
    age_filter = st.slider("Select Age Range", int(customers['age'].min()), int(customers['age'].max()), (25, 45))
    score_filter = st.slider("Select Credit Score Range", int(credit_profiles['credit_score'].min()),
                             int(credit_profiles['credit_score'].max()), (500, 750))

    merged_profiles = pd.merge(customers, credit_profiles, on="cust_id")
    filtered = merged_profiles[(merged_profiles['age'] >= age_filter[0]) & (merged_profiles['age'] <= age_filter[1]) &
                               (merged_profiles['credit_score'] >= score_filter[0]) & (
                                           merged_profiles['credit_score'] <= score_filter[1])]

    st.markdown(f"Filtered records: {len(filtered)}")
    st.dataframe(filtered.head())
