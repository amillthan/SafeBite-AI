from backend.app.services.warning_service import calculate_warning


def make_results(total, flagged):
    return (
        [{"prediction": 1, "categories": []}] * flagged
        + [{"prediction": 0, "categories": []}] * (total - flagged)
    )


def test_insufficient_data():
    result = calculate_warning(make_results(5, 4))
    assert result["warning_level"] == "Insufficient Data"


def test_high_review_signal():
    result = calculate_warning(make_results(20, 12))
    assert result["warning_level"] == "High Review Signal"


def test_moderate_review_signal():
    result = calculate_warning(make_results(20, 6))
    assert result["warning_level"] == "Moderate Review Signal"


def test_low_review_signal():
    result = calculate_warning(make_results(20, 2))
    assert result["warning_level"] == "Low Review Signal"


def test_keyword_signal_without_ml_flag():
    result = calculate_warning(
        [{"prediction": 0, "categories": ["Pest Activity"]}] * 10
    )
    assert result["flagged_reviews"] == 10


def test_empty_results():
    result = calculate_warning([])
    assert result["warning_level"] == "Insufficient Data"