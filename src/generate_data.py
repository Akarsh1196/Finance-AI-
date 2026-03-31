import pandas as pd
import numpy as np

np.random.seed(42)
n = 1000

data = []

for _ in range(n):
    income = np.random.randint(25000, 150000)

    # realistic spending behavior
    expense_ratio = np.random.uniform(0.4, 0.9)
    monthly_expense = income * expense_ratio

    rent = monthly_expense * np.random.uniform(0.2, 0.4)
    food = monthly_expense * np.random.uniform(0.1, 0.2)
    shopping = monthly_expense * np.random.uniform(0.05, 0.2)
    entertainment = monthly_expense * np.random.uniform(0.05, 0.15)

    debt = income * np.random.uniform(0, 0.5)
    investment = income * np.random.uniform(0.05, 0.3)

    savings = income - monthly_expense - debt
    savings = max(savings, 0)

    data.append([
        np.random.randint(22, 55),
        income,
        rent,
        food,
        shopping,
        entertainment,
        debt,
        investment,
        monthly_expense,
        savings
    ])

df = pd.DataFrame(data, columns=[
    'age', 'monthly_income', 'rent', 'food', 'shopping',
    'entertainment', 'debt', 'investment_amount',
    'monthly_expense', 'savings'
])

# Feature engineering
df['savings_ratio'] = df['savings'] / df['monthly_income']
df['expense_ratio'] = df['monthly_expense'] / df['monthly_income']
df['debt_to_income'] = df['debt'] / df['monthly_income']

df.to_csv('data/finance_data.csv', index=False)

print("✅ Realistic dataset created!")