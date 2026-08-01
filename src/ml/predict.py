import pickle
from pathlib import Path

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = ROOT_DIR / "models" / "provider_model.pkl"
REQUIRED_COLUMNS = ["Age", "Gender", "Medical Condition", "Admission Type"]


def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns for prediction: {missing}")

    features = df[REQUIRED_COLUMNS].copy()
    features = pd.get_dummies(features)
    return features


def predict_provider_performance(input_df: pd.DataFrame, model_path: Path | None = None) -> pd.DataFrame:
    model_path = model_path or MODEL_PATH
    with model_path.open("rb") as handle:
        artifact = pickle.load(handle)

    if isinstance(artifact, dict):
        model = artifact["model"]
        feature_columns = artifact.get("feature_columns")
    else:
        model = artifact
        feature_columns = None

    X = prepare_features(input_df)

    if feature_columns is not None:
        X = X.reindex(columns=feature_columns, fill_value=0)

    predictions = model.predict(X)
    probabilities = model.predict_proba(X)[:, 1]

    result = input_df.copy()
    result["Predicted_Long_Stay"] = predictions
    result["Risk_Probability"] = probabilities
    result["Provider_Performance_Label"] = result["Predicted_Long_Stay"].map(
        {0: "Stable", 1: "High Burden"}
    )
    return result


def predict_from_csv(csv_path: str | Path, model_path: Path | None = None) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    return predict_provider_performance(df, model_path=model_path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Predict provider performance from hospital data")
    parser.add_argument("--input", default=str(ROOT_DIR / "data" / "raw" / "hospital_raw.csv"))
    parser.add_argument("--model", default=str(MODEL_PATH))
    args = parser.parse_args()

    predictions = predict_from_csv(args.input, model_path=Path(args.model))
    print(predictions[["Age", "Gender", "Medical Condition", "Admission Type", "Risk_Probability", "Provider_Performance_Label"]].head())
