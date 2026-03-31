def generate_recommendation(financial_type, risk, user_input, simulation):

    suggestions = []

    income = user_input['income']
    expense = user_input['expense']
    savings = user_input['savings']
    debt = user_input['debt']
    investment = user_input['investment']

    # -------------------------
    # 1. Data-driven insights
    # -------------------------

    savings_ratio = savings / income if income > 0 else 0
    expense_ratio = expense / income if income > 0 else 0

    # -------------------------
    # 2. Financial Type Based
    # -------------------------

    if financial_type == 'Overspender':
        reduce_amount = int(expense * 0.2)
        suggestions.append(f"⚠️ You are overspending. Try reducing expenses by ₹{reduce_amount:,} per month.")

    elif financial_type == 'Saver':
        increase_invest = int(savings * 0.3)
        suggestions.append(f"✅ You save well. Increase investment by ₹{increase_invest:,} to grow wealth faster.")

    elif financial_type == 'Risk Taker':
        suggestions.append("⚠️ You are taking high financial risk. Balance savings and investments.")

    elif financial_type == 'Balanced':
        suggestions.append("👍 Your finances are balanced. Focus on optimizing returns.")

    # -------------------------
    # 3. Risk-Based Suggestions
    # -------------------------

    if risk == 'High':
        reduce_debt = int(debt * 0.3)
        suggestions.append(f"🚨 High risk. Try reducing debt by ₹{reduce_debt:,}.")

    elif risk == 'Medium':
        increase_savings = int(income * 0.1)
        suggestions.append(f"⚠️ Moderate risk. Increase savings by ₹{increase_savings:,} per month.")

    else:
        suggestions.append("✅ Low risk. You can explore higher return investments like mutual funds.")

    # -------------------------
    # 4. Investment Optimization
    # -------------------------

    best_option = max(simulation, key=simulation.get)
    suggestions.append(f"📈 {best_option} gives the best return for your profile.")

    # -------------------------
    # 5. Investment Gap Analysis
    # -------------------------

    recommended_investment = int(income * 0.2)

    if investment < recommended_investment:
        gap = recommended_investment - investment
        suggestions.append(f"💡 Increase your investment by ₹{gap:,} to reach optimal 20% of income.")

    return suggestions