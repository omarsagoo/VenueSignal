import argparse
import os
import tempfile
import requests

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder

feature_columns_names = [
    "review_id",
    "business_id",
    "user_id",
    "mentions_parking",
    "parking_positive",
    "parking_negative",
    "parking_type_lot",
    "parking_type_street",
    "parking_type_garage",
    "parking_type_valet",
    "parking_free",
    "parking_paid",
    "enhanced_parking_score",
    "business_stars",
    "business_review_count",
    "avg_review_stars",
    "std_review_stars",
    "total_reviews",
    "avg_engagement",
    "pct_highly_rated",
    "has_parking_data",
    "parking_sentiment",
    "review_stars",
    "useful",
    "funny",
    "cool",
    "engagement_score",
    "is_engaged",
    "review_year",
    "review_month",
    "review_quarter",
    "is_restaurant",
    "price_range_numeric",
    "event_time",
    "split",
]

label_column = "is_highly_rated"
all_columns = feature_columns_names + [label_column]

xgb_features = [
    # Business features
    "avg_review_stars",
    "std_review_stars",
    "business_review_count",
    "pct_highly_rated",
    # Parking features
    "enhanced_parking_score",
    "parking_positive",
    "parking_negative",
    "parking_sentiment",
    "has_parking_data",
    # Review engagement
    "avg_engagement",
    # Business attributes
    "is_restaurant",
    "price_range_numeric",
]

# Columns that must be numeric
numeric_cols = [
    "mentions_parking",
    "parking_positive",
    "parking_negative",
    "parking_type_lot",
    "parking_type_street",
    "parking_type_garage",
    "parking_type_valet",
    "parking_free",
    "parking_paid",
    "enhanced_parking_score",
    "business_stars",
    "business_review_count",
    "avg_review_stars",
    "std_review_stars",
    "total_reviews",
    "avg_engagement",
    "pct_highly_rated",
    "has_parking_data",
    "parking_sentiment",
    "review_stars",
    "useful",
    "funny",
    "cool",
    "engagement_score",
    "is_engaged",
    "review_year",
    "review_month",
    "review_quarter",
    "is_restaurant",
    "price_range_numeric",
    label_column,
]


def prepare_xgb_data(df: pd.DataFrame, features, target: str = "is_highly_rated") -> pd.DataFrame:
    """Prepare data in XGBoost format: target first, no header."""
    X = df[features].fillna(0)
    y = df[target]
    return pd.concat([y, X], axis=1)


def _detect_header(csv_path: str, expected_first_col: str = "review_id") -> bool:
    """Heuristic: if first cell equals the expected first column name, treat as header."""
    with open(csv_path, "r", encoding="utf-8") as f:
        first_line = f.readline().strip()

    if not first_line:
        return False

    first_cell = first_line.split(",")[0].strip().strip('"').strip("'")
    return first_cell == expected_first_col


if __name__ == "__main__":
    base_dir = "/opt/ml/processing"
    csv_path = f"{base_dir}/input/alldata.csv"

    # 1) Read CSV without forcing dtypes at read-time
    has_header = _detect_header(csv_path, expected_first_col=feature_columns_names[0])
    if has_header:
        df = pd.read_csv(csv_path, header=0)
        # Ensure we have exactly the columns we expect, in the right order
        df = df[all_columns]
    else:
        df = pd.read_csv(csv_path, header=None, names=all_columns)

    # 2) Normalize split + event_time to strings (split is used for filtering).
    df["split"] = df["split"].astype(str).str.strip().str.lower()
    df["event_time"] = df["event_time"].astype(str)

    # 3) Coerce numeric columns safely; invalid tokens become NaN.
    for c in numeric_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # 4) Impute missing numeric values (simple, deterministic).
    df[numeric_cols] = df[numeric_cols].fillna(0)

    # 5) Enforce label to 0/1 (robust if it was float/str).
    df[label_column] = (df[label_column] > 0).astype(np.int64)

    # 6) Split datasets and drop non-model fields.
    drop_cols = ["event_time", "split"]
    train_df = df[df["split"] == "train"].drop(columns=drop_cols)
    validation_df = df[df["split"] == "validation"].drop(columns=drop_cols)
    test_df = df[df["split"] == "test"].drop(columns=drop_cols)
    production_df = df[df["split"] == "production"].drop(columns=drop_cols)  # kept for parity

    # 7) Prepare XGBoost input (target first, then features; no header).
    train_xgb = prepare_xgb_data(train_df, xgb_features, target=label_column)
    val_xgb = prepare_xgb_data(validation_df, xgb_features, target=label_column)
    test_xgb = prepare_xgb_data(test_df, xgb_features, target=label_column)

    # 8) Write outputs.
    os.makedirs(f"{base_dir}/train", exist_ok=True)
    os.makedirs(f"{base_dir}/validation", exist_ok=True)
    os.makedirs(f"{base_dir}/test", exist_ok=True)

    train_xgb.to_csv(f"{base_dir}/train/train.csv", header=False, index=False)
    val_xgb.to_csv(f"{base_dir}/validation/validation.csv", header=False, index=False)
    test_xgb.to_csv(f"{base_dir}/test/test.csv", header=False, index=False)
