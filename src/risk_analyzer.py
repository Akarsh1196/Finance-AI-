import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# =========================
# 1. Load Data
# =========================
df = pd.read_csv('data/finance_data.csv')

# =========================
# 2. Create REAL Risk Score
# =========================
df['risk_score'] = (
    0.4 * df['expense_ratio'] +
    0.3 * df['debt_to_income'] -
    0.3 * df['savings_ratio']
)

# Normalize between 0 and 1
df['risk_score'] = (df['risk_score'] - df['risk_score'].min()) / (
    df['risk_score'].max() - df['risk_score'].min()
)

# Convert into categories
def categorize(score):
    if score < 0.33:
        return 'Low'
    elif score < 0.66:
        return 'Medium'
    else:
        return 'High'

df['risk_category'] = df['risk_score'].apply(categorize)

# =========================
# 3. Prepare Features
# =========================
features = [
    'savings_ratio',
    'expense_ratio',
    'debt_to_income',
    'investment_amount',
    'cluster'
]

X = df[features]
y = df['risk_category']

# =========================
# 4. Train/Test Split
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# 5. Train Model
# =========================
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# =========================
# 6. Evaluate Model
# =========================
y_pred = model.predict(X_test)

print("\n📊 Classification Report:\n")
print(classification_report(y_test, y_pred))

# =========================
# 7. Save Model
# =========================
joblib.dump(model, 'models/risk_model.pkl')

# Save updated dataset
df.to_csv('data/finance_data.csv', index=False)

print("\n✅ Risk model trained and saved successfully!")