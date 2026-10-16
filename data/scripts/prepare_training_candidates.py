
from pathlib import Path

import pandas as pd

from inspect_food_safety_candidates import SAFETY_PATTERNS

# File paths
INPUT_PATH = Path("data/raw/authorized/BDFoodSent-334k.csv")
OUTPUT_PATH = Path("data/annotations/food_safety_candidates.csv")

# Number of non-keyword reviews to sample
NEGATIVE_SAMPLE_SIZE = 12000
RANDOM_STATE = 42


def main():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {INPUT_PATH}")

    print("Loading BDFoodSent dataset...")

    df = pd.read_csv(
        INPUT_PATH,
        usecols=["uuid", "text"],
        dtype={"uuid": "string", "text": "string"},
    )

    # Remove empty reviews
    df = df.dropna(subset=["text"]).copy()
    df["text"] = df["text"].str.strip()
    df = df[df["text"].ne("")].copy()

    # Normalize text for duplicate detection
    df["normalized_text"] = (
        df["text"]
        .str.casefold()
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    # Remove duplicate reviews
    df = df.drop_duplicates(subset=["normalized_text"]).copy()

    print(f"Unique reviews: {len(df):,}")

    # Identify potential food safety reviews
    combined = pd.Series(False, index=df.index)

    for pattern in SAFETY_PATTERNS.values():
        matches = df["normalized_text"].str.contains(
            pattern,
            regex=True,
            na=False,
        )
        combined = combined | matches

    safety_candidates = df[combined].copy()
    other_candidates = df[~combined].copy()

    print(f"Potential safety candidates: {len(safety_candidates):,}")
    print(f"Other reviews: {len(other_candidates):,}")

    # Sample ordinary reviews for annotation
    sample_size = min(
        NEGATIVE_SAMPLE_SIZE,
        len(other_candidates),
    )

    other_sample = other_candidates.sample(
        n=sample_size,
        random_state=RANDOM_STATE,
    )

    # Combine both groups
    safety_candidates["candidate_source"] = "keyword_match"
    other_sample["candidate_source"] = "random_sample"

    candidates = pd.concat(
        [safety_candidates, other_sample],
        ignore_index=True,
    )

    # Randomize annotation order
    candidates = candidates.sample(
        frac=1,
        random_state=RANDOM_STATE,
    ).reset_index(drop=True)

    # Annotation columns
    candidates["label"] = ""
    candidates["category"] = ""
    candidates["annotation_status"] = "pending"

    # Keep only required columns
    candidates = candidates[
        [
            "uuid",
            "text",
            "candidate_source",
            "label",
            "category",
            "annotation_status",
        ]
    ]

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    candidates.to_csv(
        OUTPUT_PATH,
        index=False,
        encoding="utf-8-sig",
    )

    print("\n========== DATASET PREPARATION ==========")
    print(f"Keyword candidates: {len(safety_candidates):,}")
    print(f"Random review sample: {len(other_sample):,}")
    print(f"Total annotation candidates: {len(candidates):,}")
    print(f"Saved to: {OUTPUT_PATH}")

    print(
        "\nIMPORTANT: These reviews are NOT labeled yet. "
        "Both groups require manual annotation."
    )


if __name__ == "__main__":
    main()
