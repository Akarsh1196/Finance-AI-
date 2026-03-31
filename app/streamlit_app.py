import streamlit as st
import requests
import urllib.parse
import sys
import os
import pandas as pd

# Fix import for your ML pipeline
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from main_pipeline import run_pipeline

# =========================
# 🔐 LOAD SECRETS
# =========================
client_id = st.secrets["GOOGLE_CLIENT_ID"]
client_secret = st.secrets["GOOGLE_CLIENT_SECRET"]
redirect_uri = st.secrets["REDIRECT_URI"]
st.write("DEBUG REDIRECT:", redirect_uri)

# =========================
# SESSION STATE
# =========================
if "user" not in st.session_state:
    st.session_state.user = None

# =========================
# 🎨 PAGE CONFIG
# =========================
st.set_page_config(page_title="Finance AI", layout="centered")

# =========================
# 🔐 LOGIN PAGE
# =========================
if st.session_state.user is None:

    st.title("🔐 Login with Google")

    # Step 1: Create login URL
    auth_base = "https://accounts.google.com/o/oauth2/v2/auth"

    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent"
    }

    auth_url = auth_base + "?" + urllib.parse.urlencode(params)

    st.markdown(f"[👉 Click here to Login with Google]({auth_url})")

    # Step 2: Handle redirect
    query_params = st.query_params

    if "code" in query_params:
        code = query_params.get("code")

        try:
            # Step 3: Exchange code for token
            token_url = "https://oauth2.googleapis.com/token"

            data = {
                "code": code,
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code"
            }

            response = requests.post(token_url, data=data)
            token_data = response.json()

            if "access_token" in token_data:
                access_token = token_data["access_token"]

                # Step 4: Get user info
                user_info = requests.get(
                    "https://www.googleapis.com/oauth2/v2/userinfo",
                    headers={"Authorization": f"Bearer {access_token}"}
                ).json()

                # Save session
                st.session_state.user = user_info.get("email")
                st.session_state.name = user_info.get("name")
                st.session_state.picture = user_info.get("picture")

                # 🔥 clear URL + redirect
                st.query_params.clear()
                st.rerun()

            else:
                st.error("❌ Failed to fetch access token")

        except Exception as e:
            st.error("Login failed")
            st.write(e)

# =========================
# 🧠 MAIN DASHBOARD
# =========================
else:

    # Top bar
    col1, col2 = st.columns([8, 2])

    with col1:
        st.markdown(f"👤 **{st.session_state.name}**")

    with col2:
        if st.button("Logout"):
            st.session_state.user = None
            st.rerun()

    # Profile image
    if "picture" in st.session_state:
        st.image(st.session_state.picture, width=80)

    st.markdown("---")
    st.title("📊 Finance Dashboard")

    # Inputs
    col1, col2 = st.columns(2)

    with col1:
        income = st.number_input("Income (₹)", min_value=1000)
        expense = st.number_input("Expense (₹)", min_value=0)
        savings = st.number_input("Savings (₹)", min_value=0)

    with col2:
        debt = st.number_input("Debt (₹)", min_value=0)
        investment = st.number_input("Investment (₹)", min_value=0)
        years = st.slider("Years", 1, 30, 10)

    target_amount = st.number_input("🎯 Target Amount (₹)", min_value=10000, step=10000)

    if st.button("Analyze"):

        user_input = {
            'income': income,
            'expense': expense,
            'savings': savings,
            'debt': debt,
            'investment': investment,
            'years': years,
            'target_amount': target_amount
        }

        result = run_pipeline(user_input)

        st.subheader("📊 Results")

        st.write("🧠 Financial Type:", result['financial_type'])
        st.write("⚠️ Risk Level:", result['risk'])
        st.write("💰 ML Suggested:", f"₹{result['predicted_investment']:,.0f}")
        st.write("🎯 Required SIP:", f"₹{result['required_sip']:,.0f}")

        sim_df = pd.DataFrame(
            list(result['simulation'].items()),
            columns=['Type', 'Amount']
        )

        st.bar_chart(sim_df.set_index('Type'))

        st.subheader("💡 Recommendations")

        for rec in result['recommendations']:
            st.write("-", rec)