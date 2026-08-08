import os
import json
import joblib
import pandas as pd


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "backend",
    "ml",
    "models",
    "fraud_detection_model.pkl"
)

OUTPUT_PATH = os.path.join(
    BASE_DIR,
    "backend",
    "ml",
    "reports",
    "feature_importance.json"
)


def calculate_feature_importance():

    if not os.path.exists(
        MODEL_PATH
    ):

        raise FileNotFoundError(
            "Fraud detection model not found."
        )

    pipeline = joblib.load(
        MODEL_PATH
    )

    preprocessor = (
        pipeline.named_steps[
            "preprocessor"
        ]
    )

    model = (
        pipeline.named_steps[
            "classifier"
        ]
    )

    feature_names = (
        preprocessor
        .get_feature_names_out()
    )

    importance_values = (
        model.feature_importances_
    )

    importance_df = pd.DataFrame(
        {
            "feature": feature_names,
            "importance": importance_values
        }
    )

    importance_df = (
        importance_df
        .sort_values(
            "importance",
            ascending=False
        )
        .reset_index(drop=True)
    )

    importance_df[
        "importance"
    ] = importance_df[
        "importance"
    ].round(6)

    os.makedirs(
        os.path.dirname(
            OUTPUT_PATH
        ),
        exist_ok=True
    )

    importance_df.to_json(
        OUTPUT_PATH,
        orient="records",
        indent=4
    )

    print(
        "\nTop 10 Important Features"
    )

    print(
        importance_df.head(10).to_string(
            index=False
        )
    )

    print(
        f"\nSaved to: {OUTPUT_PATH}"
    )

    return importance_df


if __name__ == "__main__":

    calculate_feature_importance()
