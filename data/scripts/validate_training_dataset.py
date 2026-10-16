
from pathlib import Path

import pandas as pd

DATA_PATH = Path("data/processed/food_safety_labeled.csv")


def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Training dataset not found: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    required = {"text", "label"}
    if not required.issubset(df.columns):
        raise ValueError("Required columns: text, label")

    if df[["text", "label"]].isna().any().any():
        raise ValueError("Missing values detected")

    df["text"] = df["text"].astype(str).str.strip()

    if df["text"].eq("").any():
        raise ValueError("Empty review text detected")

    if not df["label"].isin([0, 1]).all():
        raise ValueError("Labels must be 0 or 1")

    if df["text"].str.casefold().duplicated().any():
        raise ValueError("Duplicate reviews detected")

    print(f"Total reviews: {len(df)}")
    print(f"Safety complaints: {(df['label'] == 1).sum()}")
    print(f"Non-complaints: {(df['label'] == 0).sum()}")
    print("Dataset validation passed!")


if __name__ == "__main__":
    main()
