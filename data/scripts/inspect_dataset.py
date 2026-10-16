from pathlib import Path

DATASET_DIR = Path.home() / "Downloads" / "Yelp JSON"

FILES = {
    "Business": "yelp_academic_dataset_business.json",
    "Review": "yelp_academic_dataset_review.json",
}


def main():
    print("SafeBite AI - Dataset File Inspection")
    print("-" * 40)

    for name, filename in FILES.items():
        path = DATASET_DIR / filename

        if path.is_file():
            size_gb = path.stat().st_size / (1024 ** 3)

            print(f"{name} file: FOUND")
            print(f"Size: {size_gb:.2f} GB")
        else:
            print(f"{name} file: NOT FOUND")

        print("-" * 40)


if __name__ == "__main__":
    main()