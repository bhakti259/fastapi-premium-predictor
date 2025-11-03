import pandas as pd
import pickle
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

# Load patients data
df = pd.read_json("patients.json").T  # transpose if data is in dict format

# Compute BMI and other features as in app.py
df['bmi'] = df['weight'] / (df['height'] ** 2)

def get_age_group(age):
    if age < 18:
        return 'child'
    elif 18 <= age < 65:
        return 'adult'
    return 'senior'

def get_lifestyle_risk(row):
    if row['smoker'] and row['bmi'] > 30:
        return 'high'
    elif row['smoker'] or row['bmi'] > 30:
        return 'medium'
    return 'low'

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

def get_city_tier(city):
    if city in tier_1_cities:
        return 'tier_1'
    elif city in tier_2_cities:
        return 'tier_2'
    return 'tier_3'

df['age_group'] = df['age'].apply(get_age_group)
df['lifestyle_risk'] = df.apply(get_lifestyle_risk, axis=1)
df['city_tier'] = df['city'].apply(get_city_tier)

# Features and target
X = df[['bmi', 'age_group', 'lifestyle_risk', 'city_tier']]
y = df['verdict'] if 'verdict' in df.columns else df['insurance_premium_category']  # replace with your actual target column

# Add categorical features that exist in app.py
categorical_features = ['age_group', 'lifestyle_risk', 'city_tier']
numerical_features = ['bmi']

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(), categorical_features)
    ],
    remainder='passthrough'
)

# Create pipeline
model_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Train model
model_pipeline.fit(X, y)

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump(model_pipeline, f)

print("💾 New model.pkl saved successfully!")
