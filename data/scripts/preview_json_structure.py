import json
from pathlib import Path

DATASET_DIR = Path.home() / "Downloads" / "Yelp JSON"

FILES = {
    "Business": "yelp_academic_dataset_business.json",
    "Review": "yelp_academic_dataset_review.json",
}


def inspect_structure(name, filename):
    path = DATASET_DIR / filename

    with path.open("r", encoding="utf-8") as file:
        first_line = file.readline()
        record = json.loads(first_line)

    print(f"\n{name} Dataset")
    print("-" * 40)
    print("Available columns:")

    for key in record.keys():
        print(f"  - {key}")


def main():
    print("SafeBite AI - JSON Structure Inspection")

    for name, filename in FILES.items():
        inspect_structure(name, filename)


if __name__ == "__main__":
    main()