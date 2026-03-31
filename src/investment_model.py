import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib

# Load data
df = pd.read_csv('data/finance_data.csv')

# -------------------------
# Create Target Variable
# -------------------------
# Ideal investment = function of savings & income

df['ideal_investment'] = (
    0.3 * df['savings'] +
    0.2 * df['monthly_income']
)

# -------------------------
# Features
# -------------------------
features = [
    'monthly_income',
    'monthly_expense',
    'savings',
    'debt',
    'savings_ratio',
    'expense_ratio',
    'debt_to_income'
]

X = df[features]
y = df['ideal_investment']

# -------------------------
# Train/Test Split
# -------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------
# Train Model
# -------------------------
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# -------------------------
# Evaluate
# -------------------------
preds = model.predict(X_test)
error = mean_absolute_error(y_test, preds)

print(f"📊 Mean Absolute Error: ₹{error:,.0f}")

# -------------------------
# Save Model
# -------------------------
joblib.dump(model, 'models/investment_model.pkl')

print("✅ Investment model trained and saved!")