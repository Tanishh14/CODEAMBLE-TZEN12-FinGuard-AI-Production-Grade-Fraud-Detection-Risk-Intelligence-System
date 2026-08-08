import os
import joblib
import pandas as pd
import numpy as np
import shap


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


class FraudExplainer:

    def __init__(self):

        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model not found: {MODEL_PATH}"
            )

        self.pipeline = joblib.load(
            MODEL_PATH
        )

        self.preprocessor = (
            self.pipeline.named_steps["preprocessor"]
        )

        self.model = (
            self.pipeline.named_steps["classifier"]
        )

        self.explainer = shap.TreeExplainer(
            self.model
        )

        self.feature_names = (
            self._get_feature_names()
        )

    def _get_feature_names(self):

        try:

            return list(
                self.preprocessor.get_feature_names_out()
            )

        except Exception:

            return [
                f"feature_{i}"
                for i in range(
                    self.model.n_features_in_
                )
            ]

    def explain(self, transaction):

        df = pd.DataFrame(
            [transaction]
        )

        transformed_data = (
            self.preprocessor.transform(df)
        )

        shap_values = self.explainer.shap_values(
            transformed_data
        )

        if isinstance(shap_values, list):

            values = shap_values[1][0]

        else:

            values = shap_values[0]

        values = np.asarray(
            values
        ).flatten()

        feature_names = self.feature_names

        explanation = []

        for name, value in zip(
            feature_names,
            values
        ):

            explanation.append(
                {
                    "feature": name,
                    "shap_value": round(
                        float(value),
                        6
                    ),
                    "impact": (
                        "increases_fraud_risk"
                        if value > 0
                        else "decreases_fraud_risk"
                    )
                }
            )

        explanation.sort(
            key=lambda x: abs(
                x["shap_value"]
            ),
            reverse=True
        )

        return explanation

    def top_features(
        self,
        transaction,
        top_n=5
    ):

        explanation = self.explain(
            transaction
        )

        return explanation[:top_n]


if __name__ == "__main__":

    explainer = FraudExplainer()

    transaction = {
        "amount": 15000
    }

    result = explainer.top_features(
        transaction,
        top_n=5
    )

    for item in result:

        print(
            f"{item['feature']}: "
            f"{item['shap_value']} "
            f"({item['impact']})"
        )