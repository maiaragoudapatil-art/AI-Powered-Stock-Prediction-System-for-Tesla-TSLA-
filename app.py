import streamlit as st
import json
import pandas as pd
import numpy as np

def get_prediction(data, days):
    last_price = data['Close'].iloc[-1]
    return np.linspace(last_price, last_price + 20, days)

# ---------- LOAD USERS ----------
def load_users():
    with open("users.json", "r") as f:
        return json.load(f)

def authenticate(username, password):
    users = load_users()
    return username in users and users[username] == password

# ---------- LOGIN PAGE ----------
st.title("🔐 AI Stock Prediction Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if authenticate(username, password):
        st.success("Login Successful ✅")

        # ---------- MAIN APP ----------
        st.title("📈 AI Stock Prediction System")

        # Load Data
        df = pd.read_csv("TSLA.csv")
        data = df[['Close']]

        # Dummy model loading (replace with your saved model)
        # model = load_model("rnn_model.h5")

        st.subheader("📊 Stock Price Data")
        st.line_chart(data)

        days = st.slider("Select Days to Predict", 1, 10)

        # Dummy prediction (replace with real function)
        prediction = np.random.rand(days) * 100 + data['Close'].iloc[-1]

        st.subheader("🔮 Predictions")
        st.write(prediction)

        # BUY / SELL logic
        if prediction[-1] > data['Close'].iloc[-1]:
            st.success("Recommendation: BUY 📈")
        else:
            st.error("Recommendation: SELL 📉")

    else:
        st.error("Invalid Username or Password ❌")
