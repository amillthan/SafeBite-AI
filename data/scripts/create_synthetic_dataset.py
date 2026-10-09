import csv
from pathlib import Path

OUTPUT_PATH = Path("data/processed/synthetic_reviews.csv")

reviews = [
    ("I felt sick after eating the chicken.", 1),
    ("The food was delicious and fresh.", 0),
    ("I found a hair in my meal.", 1),
    ("The staff were friendly and helpful.", 0),
    ("The restaurant kitchen looked very dirty.", 1),
    ("The restaurant had a beautiful atmosphere.", 0),
    ("I experienced stomach pain after dinner.", 1),
    ("The portions were large and satisfying.", 0),
    ("There was a cockroach near our table.", 1),
    ("The waiter provided excellent service.", 0),
    ("The meat smelled rotten.", 1),
    ("The food arrived quickly and tasted great.", 0),
    ("I noticed mold growing on the bread.", 1),
    ("The prices were reasonable.", 0),
    ("The chicken was raw in the middle.", 1),
    ("The desserts were amazing.", 0),
    ("I had vomiting and diarrhea after the meal.", 1),
    ("The dining area was clean and comfortable.", 0),
    ("There was a piece of plastic in my soup.", 1),
    ("I would definitely visit this restaurant again.", 0),
]

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["text", "label"])
    writer.writerows(reviews)

print("Synthetic dataset created successfully!")
print(f"Location: {OUTPUT_PATH}")
print(f"Total reviews: {len(reviews)}")