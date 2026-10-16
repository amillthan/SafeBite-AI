
from pathlib import Path

import pandas as pd

INPUT_PATH = Path("data/annotations/food_safety_candidates.csv")
OUTPUT_PATH = Path("data/annotations/food_safety_annotation_batch.csv")

KEYWORD_SAMPLE_SIZE = 1000
RANDOM_SAMPLE_SIZE = 1000
RANDOM_STATE = 42


def main():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"File not found: {INPUT_PATH}")

    df = pd.read_csv(
        INPUT_PATH,
        dtype={"uuid": "string", "text": "string"},
        keep_default_na=False,
    )

    required_columns = {
        "uuid",
        "text",
        "candidate_source",
        "label",
        "category",
        "annotation_status",
    }

    if not required_columns.issubset(df.columns):
        raise ValueError("Required annotation columns are missing.")

    keyword_reviews = df[
        df["candidate_source"] == "keyword_match"
    ]

    random_reviews = df[
        df["candidate_source"] == "random_sample"
    ]

    keyword_sample = keyword_reviews.sample(
        n=min(KEYWORD_SAMPLE_SIZE, len(keyword_reviews)),
        random_state=RANDOM_STATE,
    )

    random_sample = random_reviews.sample(
        n=min(RANDOM_SAMPLE_SIZE, len(random_reviews)),
        random_state=RANDOM_STATE,
    )

    batch = pd.concat(
        [keyword_sample, random_sample],
        ignore_index=True,
    )

    batch = batch.sample(
        frac=1,
        random_state=RANDOM_STATE,
    ).reset_index(drop=True)

    batch.insert(
        0,
        "annotation_id",
        [f"SB-{i:05d}" for i in range(1, len(batch) + 1)],
    )

    batch["label"] = ""
    batch["category"] = ""
    batch["annotation_status"] = "pending"

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    batch.to_csv(
        OUTPUT_PATH,
        index=False,
        encoding="utf-8-sig",
    )

    print("\n========== ANNOTATION BATCH ==========")
    print(f"Keyword candidates: {len(keyword_sample):,}")
    print(f"Random reviews: {len(random_sample):,}")
    print(f"Total reviews: {len(batch):,}")
    print(f"Saved to: {OUTPUT_PATH}")
    print("\nAll labels are pending manual annotation.")


if __name__ == "__main__":
    main()
