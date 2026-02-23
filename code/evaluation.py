import json
import pathlib
import pickle
import tarfile

import numpy as np
import pandas as pd
import xgboost
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score, roc_auc_score


def load_xgb_model(model_filename: str):
    """Load XGBoost model (Booster preferred; pickle fallback)."""
    try:
        booster = xgboost.Booster()
        booster.load_model(model_filename)
        return booster
    except Exception:
        pass

    try:
        with open(model_filename, "rb") as f:
            return pickle.load(f)
    except Exception as e:
        raise RuntimeError(
            f"Unable to load model '{model_filename}'. Expected XGBoost Booster or pickle. Error: {e}"
        )


if __name__ == "__main__":
    # Extract model artifact
    model_tar_path = "/opt/ml/processing/model/model.tar.gz"
    with tarfile.open(model_tar_path) as tar:
        tar.extractall(path=".")

    model_file = "xgboost-model"
    model = load_xgb_model(model_file)

    # Load test data (label in column 0)
    test_path = "/opt/ml/processing/test/test.csv"
    df = pd.read_csv(test_path, header=None)

    y_test = df.iloc[:, 0].to_numpy().astype(int)
    X_test = df.iloc[:, 1:].to_numpy()

    dtest = xgboost.DMatrix(X_test)

    # Predict probabilities (binary:logistic)
    probs = model.predict(dtest)

    # Convert to class predictions
    y_pred = (probs >= 0.5).astype(int)

    # Metrics
    f1 = f1_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    accuracy = accuracy_score(y_test, y_pred)

    metrics = {
        "f1": {"value": float(f1)},
        "precision": {"value": float(precision)},
        "recall": {"value": float(recall)},
        "accuracy": {"value": float(accuracy)},
    }

    # AUC only valid if both classes present
    if len(np.unique(y_test)) == 2:
        try:
            auc = roc_auc_score(y_test, probs)
            metrics["auc"] = {"value": float(auc)}
        except Exception:
            pass

    report_dict = {
        "classification_metrics": metrics
    }

    # Write evaluation output
    output_dir = "/opt/ml/processing/evaluation"
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    evaluation_path = f"{output_dir}/evaluation.json"
    with open(evaluation_path, "w") as f:
        json.dump(report_dict, f)
