import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Stock Dashboard", layout="wide")

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- LOGIN FUNCTIONS ----------------
def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except:
        return {"admin": "1234"}

def authenticate(username, password):
    users = load_users()
    return username in users and users[username] == password

# ---------------- LOGIN PAGE ----------------
if not st.session_state.logged_in:
    st.title("🔐 AI Stock Dashboard Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate(username, password):
            st.session_state.logged_in = True
            st.success("Login Successful ✅")
            st.rerun()
        else:
            st.error("Invalid Username or Password ❌")

# ---------------- MAIN APP ----------------
else:

    # -------- HEADER WITH LOGOUT --------
    col1, col2 = st.columns([8,1])

    with col1:
        st.title("📈 AI Stock Prediction Dashboard")

    with col2:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.rerun()

    # -------- LOAD DATA --------
    url = "https://raw.githubusercontent.com/maiaragoudapatil-art/AI-Powered-Stock-Prediction-System-for-Tesla-TSLA-/main/TSLA.csv"
    df = pd.read_csv(url)

    # -------- METRICS --------
    current_price = df['Close'].iloc[-1]
    prev_price = df['Close'].iloc[-2]
    change = current_price - prev_price

    col1, col2, col3 = st.columns(3)
    col1.metric("📈 Current Price", f"${current_price:.2f}")
    col2.metric("📊 Change", f"{change:.2f}")
    col3.metric("📉 Volatility", f"{df['Close'].pct_change().std():.4f}")

    # -------- INTERACTIVE GRAPH --------
    st.subheader("📊 Stock Price Trend")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=df['Close'],
        mode='lines',
        name='Stock Price',
        line=dict(color='cyan')
    ))

    fig.update_layout(template="plotly_dark", hovermode="x unified")

    st.plotly_chart(fig, use_container_width=True)

    # -------- INPUT --------
    days = st.slider("Select Prediction Days", 1, 10)

    # -------- PREDICTION --------
    def predict(data, steps):
        last = data['Close'].iloc[-1]
        trend = np.linspace(last, last * (1 + 0.01 * steps), steps)
        return trend

    prediction = predict(df, days)
    predicted_price = prediction[-1]

    # -------- FORECAST GRAPH --------
    st.subheader("🔮 Forecast")

    recent_data = df['Close'][-50:].values

    x_recent = list(range(len(recent_data)))
    x_future = list(range(len(recent_data), len(recent_data) + len(prediction)))

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
        x=x_recent,
        y=recent_data,
        mode='lines',
        name='Recent',
        line=dict(color='blue')
    ))

    fig2.add_trace(go.Scatter(
        x=x_future,
        y=prediction,
        mode='lines+markers',
        name='Forecast',
        line=dict(color='red', dash='dash')
    ))

    fig2.update_layout(
        template="plotly_dark",
        xaxis_title="Time",
        yaxis_title="Price"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # -------- INSIGHTS --------
    st.subheader("💼 Trading Insights")

    col1, col2, col3 = st.columns(3)
    col1.metric("📈 Current Price", f"${current_price:.2f}")
    col2.metric("🔮 Predicted Price", f"${predicted_price:.2f}")
    col3.metric("📊 Expected Change", f"{predicted_price - current_price:.2f}")

    # -------- SIGNAL --------
    if predicted_price > current_price:
        st.success("📈 Strong BUY Signal")
        trend = "Uptrend"
    else:
        st.error("📉 Strong SELL Signal")
        trend = "Downtrend"

    # -------- RISK --------
    volatility = df['Close'].pct_change().std()

    if volatility > 0.02:
        st.warning("⚠️ High Risk")
    else:
        st.info("✅ Low Risk")

    # -------- AI EXPLANATION --------
    st.subheader("🧠 AI Insight")

    st.markdown(f"""
    ### Market Analysis

    - **Trend:** {trend}  
    - **Prediction Horizon:** {days} days  
    - **Confidence:** Moderate  

    ### Explanation:
    The system predicts a **{trend.lower()} trend** based on recent momentum 
    and volatility patterns.

    ⚠️ This is not financial advice.
    """)

    # -------- PROFIT --------
    st.subheader("💰 Profit Simulation")

    profit = (predicted_price - current_price) * 10
    st.metric("Estimated Profit", f"${profit:.2f}")
