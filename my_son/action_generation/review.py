

class ReviewModule:
    """
    An asynchronous module that compares actual COF progress against predicted
    progress, using the CAR as a multiplier.
    """

    def generate_performance_review(self, predicted_cof_gain, actual_cof_gain, car_score):
        """
        Generates a performance review based on predicted vs. actual outcomes.

        Args:
            predicted_cof_gain (float): The predicted increase in the COF.
            actual_cof_gain (float): The actual, measured increase in the COF.
            car_score (float): The Command Adherence Rate (0.0 to 1.0).

        Returns:
            dict: A structured performance review.
        """
        if car_score == 0:
            primary_delta_cause = "Non-adherence to command. No action was taken on the prioritized directive."
        elif car_score < 1.0:
            primary_delta_cause = f"Partial adherence (CAR: {car_score*100:.0f}%). The prioritized directive was not fully executed."
        else:
            # If adherence is 100%, any delta is due to inaccurate prediction or external factors.
            prediction_accuracy = (actual_cof_gain / predicted_cof_gain) if predicted_cof_gain > 0 else 1.0
            if prediction_accuracy < 0.9:
                 primary_delta_cause = "Prediction model requires recalibration. The impact of the HVA was overestimated."
            else:
                 primary_delta_cause = "Performance as expected. COF gains are aligned with predictions."


        review = {
            'review_period': 'Last 24 hours',
            'predicted_cof_gain': round(predicted_cof_gain, 3),
            'actual_cof_gain': round(actual_cof_gain, 3),
            'command_adherence_rate': f"{car_score * 100:.1f}%",
            'primary_delta_cause': primary_delta_cause,
            'summary': f"Actual Gain: {actual_cof_gain:.2%}. Predicted Gain: {predicted_cof_gain:.2%}. Primary Delta Cause: {primary_delta_cause}"
        }
        return review

# Example Usage:
if __name__ == '__main__':
    review_module = ReviewModule()

    # --- Scenario 1: High Adherence, Good Outcome ---
    print("--- Scenario 1: High Adherence ---")
    review1 = review_module.generate_performance_review(
        predicted_cof_gain=0.25,
        actual_cof_gain=0.22,
        car_score=1.0  # User followed the command
    )
    import json
    print(json.dumps(review1, indent=2))

    # --- Scenario 2: Low Adherence, Poor Outcome ---
    print("\n--- Scenario 2: Low Adherence ---")
    review2 = review_module.generate_performance_review(
        predicted_cof_gain=0.25,
        actual_cof_gain=0.05,
        car_score=0.2  # User mostly ignored the command
    )
    print(json.dumps(review2, indent=2))

    # --- Scenario 3: Non-Adherence ---
    print("\n--- Scenario 3: Non-Adherence ---")
    review3 = review_module.generate_performance_review(
        predicted_cof_gain=0.25,
        actual_cof_gain=0.01, # Minimal gain from other, non-prioritized tasks
        car_score=0.0 # User did not follow the command at all
    )
    print(json.dumps(review3, indent=2))
