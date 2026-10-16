
from pathlib import Path

import pandas as pd

INPUT_PATH = Path("data/annotations/food_safety_annotation_batch.csv")
OUTPUT_PATH = Path("data/processed/food_safety_labeled.csv")

REQUIRED_COLUMNS = {
    "annotation_id",
    "text",
    "label",
    "annotation_status",
}


def main():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"File not found: {INPUT_PATH}")

    df = pd.read_csv(
        INPUT_PATH,
        dtype="string",
        keep_default_na=False,
    )

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    # Only include manually completed annotations
    completed = df[
        df["annotation_status"].str.strip().str.casefold()
        == "completed"
    ].copy()

    if completed.empty:
        print("No completed annotations found.")
        print("Label reviews before preparing training data.")
        return

    completed["label"] = completed["label"].str.strip()

    # Validate labels
    invalid = completed[~completed["label"].isin(["0", "1"])]

    if not invalid.empty:
        raise ValueError(
            f"{len(invalid)} completed reviews have invalid labels."
        )

    # Validate review text
    completed["text"] = completed["text"].str.strip()

    if completed["text"].eq("").any():
        raise ValueError("Completed reviews contain empty text.")

    # Prevent duplicate reviews
    completed["normalized_text"] = (
        completed["text"]
        .str.casefold()
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    completed = completed.drop_duplicates(
        subset=["normalized_text"]
    )

    # Prepare binary classification dataset
    training_df = completed[["text", "label"]].copy()

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    training_df.to_csv(
        OUTPUT_PATH,
        index=False,
        encoding="utf-8",
    )

    print("\n========== ANNOTATION VALIDATION ==========")
    print(f"Total annotation records: {len(df):,}")
    print(f"Completed annotations: {len(completed):,}")
    print(f"Training records: {len(training_df):,}")

    print("\nClass distribution:")
    print(training_df["label"].value_counts())

    print(f"\nSaved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
