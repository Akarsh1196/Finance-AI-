import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import joblib

# Load data
df = pd.read_csv('data/finance_data.csv')

# Features for clustering
features = ['savings_ratio', 'expense_ratio', 'debt_to_income', 'investment_amount']
X = df[features]

# Scale the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply KMeans
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df['cluster'] = kmeans.fit_predict(X_scaled)

# Label clusters based on savings behavior
cluster_means = df.groupby('cluster')['savings_ratio'].mean().sort_values()

label_map = {
    cluster_means.index[0]: 'Overspender',
    cluster_means.index[1]: 'Risk Taker',
    cluster_means.index[2]: 'Balanced',
    cluster_means.index[3]: 'Saver',
}

df['financial_type'] = df['cluster'].map(label_map)

# Save updated data
df.to_csv('data/finance_data.csv', index=False)

# Save models
joblib.dump(kmeans, 'models/kmeans.pkl')
joblib.dump(scaler, 'models/scaler.pkl')
joblib.dump(label_map, 'models/label_map.pkl')

print("✅ Clustering completed!")
print(df['financial_type'].value_counts())