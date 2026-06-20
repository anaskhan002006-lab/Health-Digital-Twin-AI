import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

data = pd.DataFrame({
    "Age": [25, 45, 60, 35, 55, 40, 65, 30],
    "BMI": [22, 31, 35, 24, 33, 28, 36, 23],
    "Sugar": [90, 180, 220, 100, 200, 150, 250, 95],
    "BP": [120, 150, 170, 125, 160, 145, 180, 118],
    "Disease": [0, 1, 1, 0, 1, 1, 1, 0]
})

X = data[["Age", "BMI", "Sugar", "BP"]]
y = data["Disease"]

model = RandomForestClassifier()
model.fit(X, y)

joblib.dump(model, "disease_model.pkl")

print("Model Trained Successfully")