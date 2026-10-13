import re

CATEGORY_KEYWORDS = {
    "Hygiene": [
        "dirty kitchen",
        "dirty table",
        "filthy",
        "unhygienic",
        "poor hygiene",
        "unsanitary",
    ],
    "Food Contamination": [
        "plastic in my food",
        "hair in my food",
        "glass in my food",
        "foreign object",
        "contaminated food",
        "moldy food",
    ],
    "Undercooked Food": [
        "undercooked",
        "raw chicken",
        "raw meat",
        "not cooked properly",
        "still raw",
    ],
    "Suspected Foodborne Illness": [
        "food poisoning",
        "vomiting",
        "diarrhea",
        "stomach pain",
        "felt sick after eating",
    ],
    "Pest Activity": [
        "cockroach",
        "cockroaches",
        "rat",
        "rats",
        "mouse",
        "mice",
        "rodent",
    ],
    "Food Storage": [
        "left unrefrigerated",
        "improper storage",
        "stored at room temperature",
        "spoiled food",
        "expired food",
    ],
}



NEGATION_WORDS = {
    "no",
    "not",
    "never",
    "without",
    "neither",
    "nor",
}

def is_negated(text: str, match_start: int) -> bool:
    prefix = text[:match_start]
    words = re.findall(r"\b\w+\b", prefix)

    recent_words = words[-4:]

    return any(word in NEGATION_WORDS for word in recent_words)


def detect_categories(text: str) -> list[str]:
    normalized_text = text.lower()
    detected = []

    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            pattern = rf"(?<!\w){re.escape(keyword)}(?!\w)"

            for match in re.finditer(pattern, normalized_text):
                if not is_negated(normalized_text, match.start()):
                    detected.append(category)
                    break

            if category in detected:
                break

    return detected