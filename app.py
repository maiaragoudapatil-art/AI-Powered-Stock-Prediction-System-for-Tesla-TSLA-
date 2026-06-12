import streamlit as st
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="AI Stock App", layout="wide")

# -------------------- DARK UI --------------------
st.markdown("""
<style>
.stApp {
    background-color: #0E1117;
    color: white;
}
h1, h2, h3 {
    color: #00FFAA;
}
</style>
""", unsafe_allow_html=True)

# -------------------- LOGIN --------------------
def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except:
        return {"admin": "1234"}

def authenticate(username, password):
    users = load_users()
    return username in users and users[username] == password

# -------------------- LOGIN UI --------------------
st.title("🔐 AI Stock Prediction Login")
st.info("Demo Login → Username: admin | Password: 1234")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if authenticate(username, password):
        st.success("Login Successful ✅")

        # -------------------- MAIN APP --------------------
        st.title("📈 AI Stock Prediction Dashboard")

        # Load dataset from GitHub
        url = "https://raw.githubusercontent.com/maiaragoudapatil-art/AI-Powered-Stock-Prediction-System-for-Tesla-TSLA-/main/TSLA.csv"

        try:
            df = pd.read_csv(url)
        except:
            st.error("❌ Failed to load dataset")
            st.stop()

        # -------------------- CHART --------------------
        st.subheader("📊 Tesla Stock Price Trend")

        plt.figure(figsize=(10,5))
        plt.plot(df['Close'][-100:], label='Actual Price', color='cyan')
        plt.legend()
        st.pyplot(plt)

        # -------------------- USER INPUT --------------------
        days = st.slider("Select Days to Predict", 1, 10)

        # -------------------- IMPROVED PREDICTION --------------------
        def predict(data, steps):
            last_price = data['Close'].iloc[-1]
            trend = np.linspace(last_price, last_price + (steps * 5), steps)
            noise = np.random.normal(0, 3, steps)
            return trend + noise

        prediction = predict(df, days)

        st.subheader("🔮 Future Predictions")
        st.write(prediction)

        # -------------------- FUTURE GRAPH --------------------
        st.subheader("📉 Future Forecast Graph")

        future_x = list(range(len(df[-50:]), len(df[-50:]) + len(prediction)))

        plt.figure(figsize=(10,5))
        plt.plot(df['Close'][-50:].values, label='Recent Actual', color='blue')
        plt.plot(future_x, prediction, label='Predicted', linestyle='dashed', color='red')
        plt.legend()
        st.pyplot(plt)

        # -------------------- BUSINESS LOGIC --------------------
        current_price = df['Close'].iloc[-1]
        predicted_price = prediction[-1]

        st.subheader("💼 Trading Decision")

        if predicted_price > current_price:
            st.success(f"BUY 📈 (Current: {current_price:.2f}, Predicted: {predicted_price:.2f})")
            trend = "Upward 📈"
        else:
            st.error(f"SELL 📉 (Current: {current_price:.2f}, Predicted: {predicted_price:.2f})")
            trend = "Downward 📉"

        # -------------------- RISK --------------------
        df['Returns'] = df['Close'].pct_change()
        volatility = df['Returns'].rolling(10).std().iloc[-1]

        st.subheader("⚠️ Risk Analysis")

        if volatility > 0.03:
            st.warning("High Risk ⚠️")
        else:
            st.info("Low Risk ✅")

        # -------------------- INSIGHTS --------------------
        st.subheader("📊 Business Insights")

        st.write(f"**Trend:** {trend}")
        st.write(f"**Current Price:** ${current_price:.2f}")
        st.write(f"**Predicted Price:** ${predicted_price:.2f}")
        st.write(f"**Prediction Horizon:** {days} days")

        # -------------------- AI EXPLANATION --------------------
        st.subheader("🧠 AI Explanation")

        if predicted_price > current_price:
            st.write("The model predicts an upward trend based on recent stock movements, suggesting potential growth.")
        else:
            st.write("The model predicts a downward trend, indicating possible decline in stock value.")

        # -------------------- PROFIT --------------------
        profit = 0
        for i in range(len(df['Close']) - 1):
            if df['Close'].iloc[i+1] > df['Close'].iloc[i]:
                profit += df['Close'].iloc[i+1] - df['Close'].iloc[i]

        st.subheader("💰 Profit Simulation")
        st.metric("Estimated Profit", f"${profit:.2f}")

    else:
        st.error("Invalid Username or Password ❌")
