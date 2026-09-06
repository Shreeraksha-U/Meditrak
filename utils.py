def categorize_demand(prediction):
    """
    Returns (level, recommendation, streamlit_alert_type)
    matching the thresholds documented in the README.
    """

    if prediction < 40:
        return (
            "Low",
            "Maintain minimum inventory.",
            "warning"
        )

    elif prediction < 90:
        return (
            "Moderate",
            "Maintain regular stock.",
            "info"
        )

    elif prediction < 140:
        return (
            "High",
            "Increase inventory.",
            "success"
        )

    else:
        return (
            "Very High",
            "Place a replenishment order immediately.",
            "error"
        )
