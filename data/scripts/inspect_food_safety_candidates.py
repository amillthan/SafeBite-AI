
from pathlib import Path

import pandas as pd

# Dataset location
DATA_PATH = Path("data/raw/authorized/BDFoodSent-334k.csv")

# Food safety keyword patterns
SAFETY_PATTERNS = {
    "hygiene": (
        r"\b(?:dirty|filthy|unhygienic|unsanitary|unclean|hygiene)\b"
    ),
    "food_contamination": (
        r"\b(?:mold|mould|hair|foreign object|spoiled|rotten|contaminated)\b"
    ),
    "undercooked_food": (
        r"\b(?:raw chicken|undercooked|not cooked|half cooked)\b"
    ),
    "suspected_illness": (
        r"\b(?:food poisoning|vomiting|diarrhea|diarrhoea|sick after eating)\b"
    ),
    "pest_activity": (
        r"\b(?:cockroach|rat|mouse|flies|insects|pests)\b"
    ),
    "food_storage": (
        r"\b(?:expired|stale|improper storage|bad smell)\b"
    ),
}


def main():
    # Check dataset availability
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    # Load only review text
    df = pd.read_csv(
        DATA_PATH,
        usecols=["text"],
        dtype={"text": "string"},
    )

    total_reviews = len(df)

    # Normalize review text
    normalized = (
        df["text"]
        .fillna("")
        .str.casefold()
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    # Remove empty reviews and duplicates
    normalized = normalized[
        normalized.ne("")
    ].drop_duplicates()

    unique_reviews = len(normalized)
    duplicate_count = total_reviews - unique_reviews

    print("\n========== DATASET SUMMARY ==========")
    print(f"Total reviews: {total_reviews:,}")
    print(f"Duplicate/empty reviews removed: {duplicate_count:,}")
    print(f"Unique non-empty reviews: {unique_reviews:,}")

    print("\n===== FOOD SAFETY KEYWORD MATCHES =====")

    # Track reviews matching at least one category
    combined = pd.Series(
        False,
        index=normalized.index,
        dtype=bool,
    )

    category_counts = {}

    for category, pattern in SAFETY_PATTERNS.items():
        matches = normalized.str.contains(
            pattern,
            regex=True,
            na=False,
        )

        count = int(matches.sum())
        category_counts[category] = count

        combined = combined | matches

        print(f"{category}: {count:,}")

    # Final candidate statistics
    candidate_count = int(combined.sum())
    other_count = unique_reviews - candidate_count

    candidate_percentage = (
        candidate_count / unique_reviews * 100
        if unique_reviews > 0
        else 0
    )

    print("\n========== FINAL RESULTS ==========")
    print(f"Potential food safety reviews: {candidate_count:,}")
    print(f"Other reviews: {other_count:,}")
    print(f"Potential candidate percentage: {candidate_percentage:.2f}%")

    print("\n========== IMPORTANT NOTE ==========")
    print(
        "Keyword matches are not verified food safety complaints."
    )
    print(
        "Manual annotation is required to confirm labels."
    )
    print(
        "Category counts may overlap because one review "
        "can match multiple categories."
    )


if __name__ == "__main__":
    main()
