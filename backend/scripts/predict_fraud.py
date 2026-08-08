import os
import sys
import joblib
import pandas as pd


# ============================================================
# PATH
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "backend",
    "ml",
    "models",
    "fraud_detection_model.pkl"
)


# ============================================================
# LOAD MODEL
# ============================================================

if not os.path.exists(MODEL_PATH):

    raise FileNotFoundError(
        "Fraud detection model not found.\n"
        "Run train_fraud_model.py first."
    )

model = joblib.load(
    MODEL_PATH
)


# ============================================================
# PREDICTION FUNCTION
# ============================================================

def predict_fraud(transaction):

    """
    transaction:
        dictionary containing transaction features

    Example:
        {
            "amount": 15000,
            "merchant_category": "electronics",
            "payment_method": "credit_card"
        }
    """

    df = pd.DataFrame(
        [transaction]
    )

    probability = model.predict_proba(
        df
    )[0][1]

    prediction = int(
        probability >= 0.50
    )

    risk_score = round(
        probability * 100,
        2
    )

    if probability >= 0.80:

        risk_level = "CRITICAL"

    elif probability >= 0.60:

        risk_level = "HIGH"

    elif probability >= 0.30:

        risk_level = "MEDIUM"

    else:

        risk_level = "LOW"

    return {
        "is_fraud": prediction,
        "fraud_probability": round(
            float(probability),
            4
        ),
        "risk_score": risk_score,
        "risk_level": risk_level
    }


# ============================================================
# CLI TEST
# ============================================================

if __name__ == "__main__":

    transaction = {
        "amount": 15000
    }

    result = predict_fraud(
        transaction
    )

    print("\nFinGuard AI Prediction")
    print("=" * 40)

    for key, value in result.items():

        print(
            f"{key}: {value}"
        )