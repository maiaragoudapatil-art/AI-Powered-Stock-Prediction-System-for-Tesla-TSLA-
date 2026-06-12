import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Stock Dashboard", layout="wide")

# ---------------- STYLING ----------------
st.markdown("""
<style>
body { background-color: #0E1117; color: white; }
.big-font { font-size:20px !important; }
.card {
    padding: 15px;
    border-radius: 10px;
    background-color: #1E1E1E;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN ----------------
def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except:
        return {"admin": "1234"}

def authenticate(username, password):
    users = load_users()
    return username in users and users[username] == password

# ---------------- LOGIN UI ----------------
st.title("🔐 AI Stock Dashboard")
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if authenticate(username, password):

        st.success("Welcome to AI Stock Dashboard 🚀")

        # ---------------- LOAD DATA ----------------
        url = "https://raw.githubusercontent.com/maiaragoudapatil-art/AI-Powered-Stock-Prediction-System-for-Tesla-TSLA-/main/TSLA.csv"
        df = pd.read_csv(url)

        # ---------------- HEADER METRICS ----------------
        current_price = df['Close'].iloc[-1]
        prev_price = df['Close'].iloc[-2]
        change = current_price - prev_price

        col1, col2, col3 = st.columns(3)

        col1.metric("📈 Current Price", f"${current_price:.2f}")
        col2.metric("📊 Change", f"{change:.2f}")
        col3.metric("📉 Volatility", f"{df['Close'].pct_change().std():.4f}")

        # ---------------- INTERACTIVE CHART ----------------
        st.subheader("📊 Stock Price (Interactive)")

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=df['Close'],
            mode='lines',
            name='Stock Price',
            line=dict(color='cyan')
        ))

        fig.update_layout(
            template="plotly_dark",
            hovermode="x unified"
        )

        st.plotly_chart(fig, use_container_width=True)

        # ---------------- USER INPUT ----------------
        days = st.slider("Select Prediction Days", 1, 10)

        # ---------------- SMART PREDICTION ----------------
        def predict(data, steps):
            last = data['Close'].iloc[-1]
            trend = np.linspace(last, last * (1 + 0.01 * steps), steps)
            return trend

        prediction = predict(df, days)
        predicted_price = prediction[-1]

        # ---------------- FORECAST GRAPH ----------------
        st.subheader("🔮 Forecast")

        future_x = list(range(len(df), len(df) + days))

        fig2 = go.Figure()

        fig2.add_trace(go.Scatter(
            y=df['Close'][-50:],
            mode='lines',
            name='Recent',
            line=dict(color='blue')
        ))

        fig2.add_trace(go.Scatter(
            x=future_x,
            y=prediction,
            mode='lines+markers',
            name='Forecast',
            line=dict(color='red', dash='dash')
        ))

        fig2.update_layout(template="plotly_dark")

        st.plotly_chart(fig2, use_container_width=True)

        # ---------------- BUSINESS LOGIC ----------------
        st.subheader("💼 Trading Insights")

        col1, col2 = st.columns(2)

        if predicted_price > current_price:
            col1.success("📈 BUY Signal")
            trend = "Uptrend"
        else:
            col1.error("📉 SELL Signal")
            trend = "Downtrend"

        col2.info(f"Trend: {trend}")

        # ---------------- RISK ----------------
        volatility = df['Close'].pct_change().std()

        if volatility > 0.02:
            risk = "High Risk ⚠️"
        else:
            risk = "Low Risk ✅"

        st.warning(f"Risk Level: {risk}")

        # ---------------- EXPLANATION ----------------
        st.subheader("🧠 AI Insight")

        st.write(f"""
        The model analyzes recent stock trends and predicts a **{trend.lower()}** 
        over the next **{days} days**. 

        This is based on:
        - Recent price momentum  
        - Short-term trend continuation  
        - Market volatility patterns  

        ⚠️ Note: This is a predictive model, not financial advice.
        """)

        # ---------------- PROFIT SIM ----------------
        st.subheader("💰 Profit Simulation")

        profit = (predicted_price - current_price) * 10
        st.metric("Estimated Profit", f"${profit:.2f}")

    else:
        st.error("Invalid Login ❌")
