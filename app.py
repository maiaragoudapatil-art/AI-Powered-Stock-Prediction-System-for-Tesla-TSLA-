import streamlit as st
import pandas as pd
import numpy as np
import json

# -------------------- LOGIN SYSTEM --------------------

def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except:
        return {"admin": "1234"}  # fallback user

def authenticate(username, password):
    users = load_users()
    return username in users and users[username] == password

# -------------------- UI --------------------

st.set_page_config(page_title="AI Stock Prediction", layout="wide")

st.title("🔐 AI Stock Prediction Login")

st.info("Demo Login → Username: admin | Password: 1234")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if authenticate(username, password):
        st.success("Login Successful ✅")

        # -------------------- MAIN APP --------------------

        st.title("📈 AI Stock Prediction System")

        # Load dataset from GitHub
        url = "https://raw.githubusercontent.com/maiaragoudapatil-art/AI-Powered-Stock-Prediction-System-for-Tesla-TSLA-/main/TSLA.csv"

        try:
            df = pd.read_csv(url)
        except:
            st.error("❌ Failed to load dataset")
            st.stop()

        # Show data
        st.subheader("📊 Tesla Stock Data")
        st.line_chart(df['Close'])

        # -------------------- USER INPUT --------------------

        days = st.slider("Select Days to Predict", 1, 10)

        # -------------------- PREDICTION (SIMULATED) --------------------

        def predict(data, steps):
            last_price = data['Close'].iloc[-1]
            trend = np.linspace(last_price, last_price + 20, steps)
            noise = np.random.normal(0, 2, steps)
            return trend + noise

        prediction = predict(df, days)

        st.subheader("🔮 Future Predictions")
        st.write(prediction)

        # -------------------- BUSINESS LOGIC --------------------

        current_price = df['Close'].iloc[-1]
        predicted_price = prediction[-1]

        st.subheader("💼 Trading Decision")

        if predicted_price > current_price:
            st.success(f"BUY 📈 (Current: {current_price:.2f}, Predicted: {predicted_price:.2f})")
        else:
            st.error(f"SELL 📉 (Current: {current_price:.2f}, Predicted: {predicted_price:.2f})")

        # -------------------- RISK LEVEL --------------------

        df['Returns'] = df['Close'].pct_change()
        volatility = df['Returns'].rolling(10).std().iloc[-1]

        st.subheader("⚠️ Risk Analysis")

        if volatility > 0.03:
            st.warning("High Risk ⚠️")
        else:
            st.info("Low Risk ✅")

        # -------------------- PROFIT SIMULATION --------------------

        st.subheader("💰 Profit Simulation")

        profit = 0
        for i in range(len(df['Close']) - 1):
            if df['Close'].iloc[i+1] > df['Close'].iloc[i]:
                profit += df['Close'].iloc[i+1] - df['Close'].iloc[i]

        st.write(f"Simulated Profit: ${profit:.2f}")

    else:
        st.error("Invalid Username or Password ❌")
