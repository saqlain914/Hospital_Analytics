import pickle
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT_DIR / "data" / "raw" / "hospital_raw.csv"
MODEL_PATH = ROOT_DIR / "models" / "provider_model.pkl"


def train_provider_model():
    # Load your clean local data
    df = pd.read_csv(DATA_PATH)

    # Feature Engineering: Calculate Length of Stay
    df["Date of Admission"] = pd.to_datetime(df["Date of Admission"], errors="coerce")
    df["Discharge Date"] = pd.to_datetime(df["Discharge Date"], errors="coerce")
    df["Length_of_Stay"] = (df["Discharge Date"] - df["Date of Admission"]).dt.days

    # Target: High Stay (e.g., above median stay duration)
    df["Is_Long_Stay"] = (df["Length_of_Stay"] > df["Length_of_Stay"].median()).astype(int)

    # Features to predict provider burden
    X = pd.get_dummies(df[["Age", "Gender", "Medical Condition", "Admission Type"]])
    y = df["Is_Long_Stay"]

    # Train model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Save the trained model and the expected feature columns
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    artifact = {"model": model, "feature_columns": list(X.columns)}
    with MODEL_PATH.open("wb") as handle:
        pickle.dump(artifact, handle)
    print(f"Provider model trained and saved as '{MODEL_PATH}'.")


if __name__ == "__main__":
    train_provider_model()
