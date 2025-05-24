import os
import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Create model directory if doesn't exist
MODEL_DIR = 'backend/model'
os.makedirs(MODEL_DIR, exist_ok=True)

# Sample dummy data - Replace this with your real data loading logic
data = {
    'age': [25, 45, 35, 52, 23, 40, 60, 30],
    'location': ['Urban', 'Rural', 'Urban', 'Urban', 'Rural', 'Urban', 'Rural', 'Urban'],
    'income': [50000, 30000, 40000, 60000, 28000, 52000, 27000, 45000],
    'interaction_count': [5, 2, 3, 6, 1, 7, 0, 4],
    'interest_score': [0.7, 0.4, 0.6, 0.8, 0.3, 0.75, 0.2, 0.65],
    'converted': [1, 0, 1, 1, 0, 1, 0, 1]  # Target: 1=converted lead, 0=not converted
}

df = pd.DataFrame(data)

# Encode location
encoder = LabelEncoder()
df['location'] = encoder.fit_transform(df['location'])

X = df.drop('converted', axis=1)
y = df['converted']

# Train-test split (optional here, but good practice)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model training - Random Forest classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model and encoder
with open(os.path.join(MODEL_DIR, 'lead_model.pkl'), 'wb') as f:
    pickle.dump(model, f)

with open(os.path.join(MODEL_DIR, 'location_encoder.pkl'), 'wb') as f:
    pickle.dump(encoder, f)

print("Model and encoder saved successfully!")
