from .shap_explainer import FraudExplainer


class ExplanationService:

    def __init__(self):

        self.explainer = FraudExplainer()

    def generate_explanation(
        self,
        transaction,
        fraud_probability
    ):

        top_features = (
            self.explainer.top_features(
                transaction,
                top_n=5
            )
        )

        risk_score = round(
            fraud_probability * 100,
            2
        )

        if fraud_probability >= 0.80:

            risk_level = "CRITICAL"

        elif fraud_probability >= 0.60:

            risk_level = "HIGH"

        elif fraud_probability >= 0.30:

            risk_level = "MEDIUM"

        else:

            risk_level = "LOW"

        reasons = []

        for feature in top_features:

            feature_name = (
                feature["feature"]
            )

            shap_value = (
                feature["shap_value"]
            )

            if shap_value > 0:

                reasons.append(
                    f"{feature_name} "
                    f"increased the fraud risk"
                )

            else:

                reasons.append(
                    f"{feature_name} "
                    f"reduced the fraud risk"
                )

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "fraud_probability": round(
                fraud_probability,
                4
            ),
            "top_risk_factors": reasons,
            "feature_contributions": top_features
        }


def explain_transaction(
    transaction,
    fraud_probability
):

    service = ExplanationService()

    return service.generate_explanation(
        transaction,
        fraud_probability
    )


if __name__ == "__main__":

    transaction = {
        "amount": 15000
    }

    result = explain_transaction(
        transaction,
        0.87
    )

    print("\nFinGuard AI Explanation")
    print("=" * 50)

    print(
        f"Risk Score: "
        f"{result['risk_score']}"
    )

    print(
        f"Risk Level: "
        f"{result['risk_level']}"
    )

    print("\nReasons:")

    for reason in result[
        "top_risk_factors"
    ]:

        print(
            f"- {reason}"
        )
