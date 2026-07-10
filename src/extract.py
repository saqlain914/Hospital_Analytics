"""
extract.py
----------
Step 1 of the ETL pipeline: EXTRACT

Downloads the Hospital Management Dataset from Kaggle using the kagglehub API:
https://www.kaggle.com/datasets/kanakbaghel/hospital-management-dataset

If kagglehub / Kaggle credentials are not available (e.g. no internet access,
no ~/.kaggle/kaggle.json configured), this script falls back to generating a
synthetic dataset with an identical schema so the rest of the pipeline can
still be developed and tested end-to-end. Replace the fallback with the real
download once you have Kaggle API credentials configured.

To use the real Kaggle download:
    1. pip install kagglehub
    2. Get your Kaggle API token from https://www.kaggle.com/settings -> "Create New Token"
    3. Place kaggle.json at ~/.kaggle/kaggle.json (or set KAGGLE_USERNAME / KAGGLE_KEY env vars)
    4. Run this script
"""

import os
import shutil
import sys
from pathlib import Path

import pandas as pd

RAW_DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

KAGGLE_DATASET = "kanakbaghel/hospital-management-dataset"
OUTPUT_FILE = RAW_DATA_DIR / "hospital_raw.csv"


def download_from_kaggle() -> Path | None:
    """Attempt to download the dataset using kagglehub. Returns path to CSV or None on failure."""
    try:
        import kagglehub

        print(f"Downloading dataset '{KAGGLE_DATASET}' from Kaggle...")
        dataset_path = kagglehub.dataset_download(KAGGLE_DATASET)
        print(f"Dataset downloaded to: {dataset_path}")

        csv_files = list(Path(dataset_path).glob("*.csv"))
        if not csv_files:
            print("No CSV file found in downloaded dataset.")
            return None

        source_csv = csv_files[0]
        shutil.copy(source_csv, OUTPUT_FILE)
        print(f"Copied raw data to: {OUTPUT_FILE}")
        return OUTPUT_FILE

    except Exception as e:
        print(f"Kaggle download failed or not configured: {e}")
        return None


def generate_synthetic_fallback(n_rows: int = 5000) -> Path:
    """
    Generates a synthetic dataset matching the schema of the Kaggle
    Hospital Management Dataset so the pipeline is fully runnable offline.
    """
    import numpy as np
    from datetime import timedelta
    import random

    print(f"Falling back to synthetic data generation ({n_rows} rows)...")

    try:
        from faker import Faker
        fake = Faker()
        Faker.seed(42)
    except ImportError:
        print("Faker not installed; install via 'pip install Faker' for realistic names.")
        raise

    np.random.seed(42)
    random.seed(42)

    genders = ["Male", "Female"]
    blood_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    conditions = ["Diabetes", "Hypertension", "Asthma", "Cancer", "Obesity", "Arthritis"]
    doctors = [fake.name() for _ in range(40)]
    hospitals = [f"{fake.last_name()} Medical Center" for _ in range(15)]
    insurance_providers = ["Aetna", "Blue Cross", "Cigna", "Medicare", "UnitedHealthcare"]
    admission_types = ["Emergency", "Elective", "Urgent"]
    medications = ["Aspirin", "Ibuprofen", "Penicillin", "Paracetamol", "Lipitor"]
    test_results = ["Normal", "Abnormal", "Inconclusive"]
    departments = ["Cardiology", "Neurology", "Orthopedics", "Pediatrics",
                   "Oncology", "General Medicine", "Emergency"]

    start_date = pd.Timestamp("2022-01-01")
    end_date = pd.Timestamp("2024-12-31")
    date_range_days = (end_date - start_date).days

    rows = []
    for _ in range(n_rows):
        admission_date = start_date + timedelta(days=random.randint(0, date_range_days))
        stay_length = random.randint(1, 20)
        discharge_date = admission_date + timedelta(days=stay_length)

        rows.append({
            "Name": fake.name(),
            "Age": random.randint(0, 95),
            "Gender": random.choice(genders),
            "Blood Type": random.choice(blood_types),
            "Medical Condition": random.choice(conditions),
            "Date of Admission": admission_date.strftime("%Y-%m-%d"),
            "Doctor": random.choice(doctors),
            "Hospital": random.choice(hospitals),
            "Department": random.choice(departments),
            "Insurance Provider": random.choice(insurance_providers),
            "Billing Amount": round(random.uniform(500, 55000), 2),
            "Room Number": random.randint(100, 999),
            "Admission Type": random.choice(admission_types),
            "Discharge Date": discharge_date.strftime("%Y-%m-%d"),
            "Medication": random.choice(medications),
            "Test Results": random.choice(test_results),
        })

    # Intentionally inject some messiness for the transform step to clean
    df = pd.DataFrame(rows)
    dup_sample = df.sample(frac=0.02, random_state=1)
    df = pd.concat([df, dup_sample], ignore_index=True)  # duplicates

    for col in ["Billing Amount", "Insurance Provider", "Age"]:
        missing_idx = df.sample(frac=0.01, random_state=2).index
        df.loc[missing_idx, col] = None

    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Synthetic raw dataset written to: {OUTPUT_FILE}")
    return OUTPUT_FILE


def main():
    path = download_from_kaggle()
    if path is None:
        path = generate_synthetic_fallback()

    df = pd.read_csv(path)
    print(f"\nRaw dataset shape: {df.shape}")
    print(df.head())
    return path


if __name__ == "__main__":
    main()
