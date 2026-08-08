import os
import json
import warnings
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    classification_report,
)

warnings.filterwarnings("ignore")


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

DATA_PATH = os.path.join(BASE_DIR, "data", "transactions.csv")

MODEL_DIR = os.path.join(BASE_DIR, "backend", "ml", "models")
REPORT_DIR = os.path.join(BASE_DIR, "backend", "ml", "reports")

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)


MODEL_PATH = os.path.join(
    MODEL_DIR,
    "fraud_detection_model.pkl"
)

PREPROCESSOR_PATH = os.path.join(
    MODEL_DIR,
    "preprocessor.pkl"
)

FEATURES_PATH = os.path.join(
    MODEL_DIR,
    "feature_columns.json"
)


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 60)
print("FinGuard AI - Fraud Detection Training")
print("=" * 60)

print("\n[1/8] Loading dataset...")

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(
        f"\nDataset not found:\n{DATA_PATH}\n\n"
        "Place your dataset at:\n"
        "data/transactions.csv"
    )

df = pd.read_csv(DATA_PATH)

print(f"Dataset shape: {df.shape}")
print(f"Columns: {list(df.columns)}")


# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
)


# ============================================================
# DETECT TARGET COLUMN
# ============================================================

print("\n[2/8] Detecting target column...")

possible_targets = [
    "is_fraud",
    "fraud",
    "fraud_flag",
    "fraudulent",
    "is_fraudulent",
    "target",
    "label",
    "class"
]

target_column = None

for column in possible_targets:
    if column in df.columns:
        target_column = column
        break

if target_column is None:
    raise ValueError(
        "\nCould not find fraud target column.\n"
        "Expected one of:\n"
        f"{possible_targets}\n\n"
        f"Available columns:\n{list(df.columns)}"
    )

print(f"Target column: {target_column}")


# ============================================================
# TARGET CLEANING
# ============================================================

def convert_target(value):

    if pd.isna(value):
        return np.nan

    if isinstance(value, str):

        value = value.strip().lower()

        fraud_values = [
            "1",
            "true",
            "yes",
            "fraud",
            "fraudulent",
            "positive"
        ]

        legitimate_values = [
            "0",
            "false",
            "no",
            "legitimate",
            "normal",
            "non-fraud",
            "non_fraud",
            "negative"
        ]

        if value in fraud_values:
            return 1

        if value in legitimate_values:
            return 0

    try:
        value = float(value)

        if value in [0, 1]:
            return int(value)

    except Exception:
        pass

    return np.nan


df[target_column] = df[target_column].apply(convert_target)

df = df.dropna(subset=[target_column])

df[target_column] = df[target_column].astype(int)

print("\nTarget distribution:")
print(df[target_column].value_counts())

fraud_count = int((df[target_column] == 1).sum())
legitimate_count = int((df[target_column] == 0).sum())

print(f"Legitimate transactions: {legitimate_count}")
print(f"Fraudulent transactions: {fraud_count}")


# ============================================================
# REMOVE ID / LEAKAGE COLUMNS
# ============================================================

print("\n[3/8] Preparing features...")

drop_columns = [
    target_column,

    # IDs
    "transaction_id",
    "transactionid",
    "id",
    "customer_id",
    "user_id",
    "account_id",
    "device_id",

    # Direct labels
    "fraud_reason",
    "fraud_type",
    "fraud_score",
]

drop_columns = [
    column
    for column in drop_columns
    if column in df.columns
]

X = df.drop(columns=drop_columns)
y = df[target_column]

print(f"Features before preprocessing: {X.shape[1]}")


# ============================================================
# REMOVE HIGH-CARDINALITY COLUMNS
# ============================================================

high_cardinality_columns = []

for column in X.columns:

    unique_ratio = X[column].nunique() / max(len(X), 1)

    if X[column].dtype == "object" and unique_ratio > 0.80:
        high_cardinality_columns.append(column)

if high_cardinality_columns:

    print(
        "\nRemoving high-cardinality columns:"
    )

    for column in high_cardinality_columns:
        print(f"  - {column}")

    X = X.drop(columns=high_cardinality_columns)


# ============================================================
# TRAIN TEST SPLIT
# ============================================================

print("\n[4/8] Splitting dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print(f"Training samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")


# ============================================================
# IDENTIFY DATA TYPES
# ============================================================

numeric_features = X_train.select_dtypes(
    include=["int64", "int32", "float64", "float32"]
).columns.tolist()

categorical_features = X_train.select_dtypes(
    include=["object", "category", "bool"]
).columns.tolist()

print("\nNumeric features:")
print(numeric_features)

print("\nCategorical features:")
print(categorical_features)


# ============================================================
# PREPROCESSING
# ============================================================

print("\n[5/8] Building preprocessing pipeline...")

numeric_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="median")
        ),
        (
            "scaler",
            StandardScaler()
        )
    ]
)

categorical_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="most_frequent")
        ),
        (
            "encoder",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            )
        )
    ]
)

transformers = []

if numeric_features:

    transformers.append(
        (
            "numeric",
            numeric_pipeline,
            numeric_features
        )
    )

if categorical_features:

    transformers.append(
        (
            "categorical",
            categorical_pipeline,
            categorical_features
        )
    )

preprocessor = ColumnTransformer(
    transformers=transformers,
    remainder="drop"
)


# ============================================================
# MODEL
# ============================================================

print("\n[6/8] Building Random Forest model...")

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    class_weight="balanced_subsample",
    random_state=42,
    n_jobs=-1
)

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", model)
    ]
)


# ============================================================
# TRAIN
# ============================================================

print("\nTraining model...")

pipeline.fit(
    X_train,
    y_train
)

print("Training completed.")


# ============================================================
# EVALUATION
# ============================================================

print("\n[7/8] Evaluating model...")

y_pred = pipeline.predict(X_test)

y_probability = pipeline.predict_proba(X_test)[:, 1]


accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)

roc_auc = roc_auc_score(
    y_test,
    y_probability
)

pr_auc = average_precision_score(
    y_test,
    y_probability
)

cm = confusion_matrix(
    y_test,
    y_pred
)

print("\n" + "=" * 60)
print("MODEL PERFORMANCE")
print("=" * 60)

print(f"Accuracy   : {accuracy:.4f}")
print(f"Precision  : {precision:.4f}")
print(f"Recall     : {recall:.4f}")
print(f"F1 Score   : {f1:.4f}")
print(f"ROC-AUC    : {roc_auc:.4f}")
print(f"PR-AUC     : {pr_auc:.4f}")

print("\nConfusion Matrix:")
print(cm)

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=[
            "Legitimate",
            "Fraud"
        ],
        zero_division=0
    )
)


# ============================================================
# SAVE MODEL
# ============================================================

print("\n[8/8] Saving model...")

joblib.dump(
    pipeline,
    MODEL_PATH
)

feature_columns = {
    "numeric_features": numeric_features,
    "categorical_features": categorical_features,
    "removed_columns": drop_columns,
    "target_column": target_column
}

with open(
    FEATURES_PATH,
    "w"
) as file:

    json.dump(
        feature_columns,
        file,
        indent=4
    )


# ============================================================
# SAVE REPORT
# ============================================================

metrics = {
    "accuracy": float(accuracy),
    "precision": float(precision),
    "recall": float(recall),
    "f1_score": float(f1),
    "roc_auc": float(roc_auc),
    "pr_auc": float(pr_auc),
    "training_samples": int(len(X_train)),
    "testing_samples": int(len(X_test)),
    "fraud_samples": fraud_count,
    "legitimate_samples": legitimate_count
}

metrics_path = os.path.join(
    REPORT_DIR,
    "training_metrics.json"
)

with open(
    metrics_path,
    "w"
) as file:

    json.dump(
        metrics,
        file,
        indent=4
    )


print("\n" + "=" * 60)
print("TRAINING COMPLETE")
print("=" * 60)

print(f"\nModel saved to:")
print(MODEL_PATH)

print(f"\nMetrics saved to:")
print(metrics_path)

print("\nFinGuard AI model is ready.")