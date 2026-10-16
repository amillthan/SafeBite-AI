from backend.app.services.category_service import detect_categories


def test_single_category():
    review = "I found a cockroach in my food."
    assert detect_categories(review) == ["Pest Activity"]


def test_multiple_categories():
    review = "The kitchen was filthy and I saw cockroaches."
    assert detect_categories(review) == [
        "Hygiene",
        "Pest Activity",
    ]


def test_no_category():
    review = "The restaurant had friendly staff and delicious food."
    assert detect_categories(review) == []


def test_case_insensitive():
    review = "THE CHICKEN WAS UNDERCOOKED."
    assert detect_categories(review) == ["Undercooked Food"]


def test_no_partial_word_matching():
    review = "The restaurant has a rating system."
    assert detect_categories(review) == []