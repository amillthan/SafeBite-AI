def calculate_warning(results: list[dict]) -> dict:
    total = len(results)

    if total == 0:
        return {
            "total_reviews": 0,
            "flagged_reviews": 0,
            "complaint_rate": 0.0,
            "warning_level": "Insufficient Data",
        }

    flagged = sum(
        1
        for result in results
        if result["prediction"] == 1
        or bool(result.get("categories"))
    )

    complaint_rate = round(flagged / total * 100, 2)

    if total < 10:
        warning_level = "Insufficient Data"
    elif complaint_rate >= 50:
        warning_level = "High Review Signal"
    elif complaint_rate >= 25:
        warning_level = "Moderate Review Signal"
    else:
        warning_level = "Low Review Signal"

    return {
        "total_reviews": total,
        "flagged_reviews": flagged,
        "complaint_rate": complaint_rate,
        "warning_level": warning_level,
    }