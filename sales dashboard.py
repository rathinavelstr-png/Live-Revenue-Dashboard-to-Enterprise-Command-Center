import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Live Dashboard", layout="wide")

st.title("📊 Live Command Center")

# -----------------------------
# DATA STORAGE
# -----------------------------
if "sales" not in st.session_state:
    st.session_state.sales = pd.DataFrame(
        columns=["time","product","price","city"]
    )

if "hospital" not in st.session_state:
    st.session_state.hospital = pd.DataFrame(
        columns=["time","patientid","triage","wait","department"]
    )

# -----------------------------
# OPTIONS
# -----------------------------
dashboard = st.sidebar.selectbox(
    "Select Dashboard",
    ["Live Revenue", "Hospital ER"]
)

refresh = st.sidebar.slider("Refresh Seconds", 5, 60, 10)

# -----------------------------
# SAMPLE DATA
# -----------------------------
products = ["Laptop","Mobile","Tablet","Camera"]
cities = ["Chennai","Mumbai","Delhi","Bangalore"]
departments = ["Emergency","Cardiology","General"]

def generate_sale():
    return {
        "time": datetime.now(),
        "product": random.choice(products),
        "price": random.randint(2000,50000),
        "city": random.choice(cities)
    }

def generate_patient():
    return {
        "time": datetime.now(),
        "patientid": random.randint(1000,9999),
        "triage": random.randint(1,5),
        "wait": random.randint(5,120),
        "department": random.choice(departments)
    }

# -----------------------------
# SALES DASHBOARD
# -----------------------------
if dashboard == "Live Revenue":

    st.header("📈 Live Revenue")

    # Add new data
    new = generate_sale()
    st.session_state.sales = pd.concat(
        [st.session_state.sales, pd.DataFrame([new])],
        ignore_index=True
    )

    df = st.session_state.sales

    # Metrics
    col1,col2,col3 = st.columns(3)
    col1.metric("Revenue", f"₹{df['price'].sum():,}")
    col2.metric("Orders", len(df))
    col3.metric("Avg", int(df["price"].mean()))

    # Charts
    st.plotly_chart(px.bar(df, x="city", y="price", title="City Sales"), use_container_width=True)
    st.plotly_chart(px.pie(df, names="product", title="Product Share"), use_container_width=True)

    # Table
    st.dataframe(df.tail(10))

# -----------------------------
# HOSPITAL DASHBOARD
# -----------------------------
if dashboard == "Hospital ER":

    st.header("🏥 Hospital ER")

    # Add new data
    new = generate_patient()
    st.session_state.hospital = pd.concat(
        [st.session_state.hospital, pd.DataFrame([new])],
        ignore_index=True
    )

    df = st.session_state.hospital

    # Metrics
    col1,col2,col3 = st.columns(3)
    col1.metric("Patients", len(df))
    col2.metric("Avg Wait", int(df["wait"].mean()))
    col3.metric("Critical", len(df[df["triage"]==1]))

    # Charts
    st.plotly_chart(px.bar(df, x="department", y="wait", title="Department Load"), use_container_width=True)
    st.plotly_chart(px.histogram(df, x="triage", title="Triage"), use_container_width=True)

    # Table
    st.dataframe(df.tail(10))

# -----------------------------
# AUTO REFRESH
# -----------------------------
time.sleep(refresh)
st.rerun()
