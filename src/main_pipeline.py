import joblib
import numpy as np

from simulator import simulate_all, required_monthly_investment
from recommendation import generate_recommendation

# -------------------------
# Load Models
# -------------------------
kmeans = joblib.load('models/kmeans.pkl')
scaler = joblib.load('models/scaler.pkl')
label_map = joblib.load('models/label_map.pkl')
risk_model = joblib.load('models/risk_model.pkl')
investment_model = joblib.load('models/investment_model.pkl')


def run_pipeline(user_input):

    # -------------------------
    # Feature Engineering
    # -------------------------
    income = user_input['income']
    expense = user_input['expense']
    savings = user_input['savings']
    debt = user_input['debt']
    investment_amount = user_input['investment']

    savings_ratio = savings / income if income > 0 else 0
    expense_ratio = expense / income if income > 0 else 0
    debt_to_income = debt / income if income > 0 else 0

    # -------------------------
    # Clustering
    # -------------------------
    X_cluster = np.array([[savings_ratio, expense_ratio, debt_to_income, investment_amount]])
    X_scaled = scaler.transform(X_cluster)

    cluster = kmeans.predict(X_scaled)[0]
    financial_type = label_map[cluster]

    # -------------------------
    # Risk Prediction
    # -------------------------
    risk_features = np.array([[
        savings_ratio,
        expense_ratio,
        debt_to_income,
        investment_amount,
        cluster
    ]])

    risk = risk_model.predict(risk_features)[0]

    # -------------------------
    # Investment Simulation
    # -------------------------
    simulation = simulate_all(investment_amount, user_input['years'])

    # -------------------------
    # 🧠 ML Investment Prediction
    # -------------------------
    invest_features = np.array([[
        income,
        expense,
        savings,
        debt,
        savings_ratio,
        expense_ratio,
        debt_to_income
    ]])

    predicted_investment = investment_model.predict(invest_features)[0]

    # -------------------------
    # Goal-Based Planning
    # -------------------------
    target_amount = user_input['target_amount']

    required_sip = required_monthly_investment(
        target_amount,
        12,
        user_input['years']
    )

    # -------------------------
    # Recommendation Engine
    # -------------------------
    recommendations = generate_recommendation(
        financial_type,
        risk,
        user_input,
        simulation
    )

    # -------------------------
    # Final Output
    # -------------------------
    return {
        'financial_type': financial_type,
        'risk': risk,
        'simulation': simulation,
        'recommendations': recommendations,
        'target_amount': target_amount,
        'required_sip': required_sip,
        'predicted_investment': predicted_investment
    }


# Test run
if __name__ == "__main__":

    user = {
        'income': 80000,
        'expense': 50000,
        'savings': 20000,
        'debt': 10000,
        'investment': 10000,
        'years': 10,
        'target_amount': 10000000
    }

    result = run_pipeline(user)

    print("\n🧠 Financial Type:", result['financial_type'])
    print("⚠️ Risk Level:", result['risk'])

    print("\n📊 Investment Results:")
    for k, v in result['simulation'].items():
        print(f"{k}: ₹{v:,.0f}")

    print(f"\n🎯 Target Amount: ₹{result['target_amount']:,.0f}")
    print(f"Required SIP: ₹{result['required_sip']:,.0f}")

    print(f"\n🧠 ML Suggested Investment: ₹{result['predicted_investment']:,.0f}")

    print("\n💡 Recommendations:")
    for rec in result['recommendations']:
        print("-", rec)