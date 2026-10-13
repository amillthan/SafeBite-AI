import pytest

from backend.app.services.category_service import detect_categories


@pytest.mark.parametrize(
    "review, expected",
    [
        ("I saw cockroaches in the kitchen.", ["Pest Activity"]),
        ("I did not see any cockroaches.", []),
        ("There were no rats in the restaurant.", []),
        ("The kitchen was filthy.", ["Hygiene"]),
        ("The chicken was undercooked.", ["Undercooked Food"]),
        (
            "The kitchen was filthy and I saw cockroaches.",
            ["Hygiene", "Pest Activity"],
        ),
    ],
)
def test_category_detection_with_negation(review, expected):
    assert detect_categories(review) == expected