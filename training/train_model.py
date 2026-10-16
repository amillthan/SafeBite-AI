
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

# --------------------------------------------------
# 1. File paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR / "data" / "annotations" /
    "SafeBite_AI_labeled_501.csv"
)

MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = MODEL_DIR / "safebite_binary_model.joblib"

# --------------------------------------------------
# 2. Load and validate dataset
# --------------------------------------------------

df = pd.read_csv(DATA_PATH, keep_default_na=False)

df["text"] = df["text"].astype(str).str.strip()
df["label"] = df["label"].astype(str).str.strip()

df = df[
    (df["text"] != "") &
    (df["label"].isin(["0", "1"]))
].copy()

df["label"] = df["label"].astype(int)

# Prevent identical reviews appearing in multiple splits
df = df.drop_duplicates(subset=["text"]).copy()

print("Total usable reviews:", len(df))
print("\nLabel distribution:")
print(df["label"].value_counts())

# --------------------------------------------------
# 3. Split dataset (70/15/15)
# --------------------------------------------------

X = df["text"]
y = df["label"]

X_train, X_temp, y_train, y_temp = train_test_split(
    X, y,
    test_size=0.30,
    random_state=42,
    stratify=y,
)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp,
    test_size=0.50,
    random_state=42,
    stratify=y_temp,
)

print("\nDataset split:")
print("Training:", len(X_train))
print("Validation:", len(X_val))
print("Testing:", len(X_test))

# --------------------------------------------------
# 4. Create model pipeline
# --------------------------------------------------

model = Pipeline([
    ("tfidf", TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        sublinear_tf=True,
        max_features=10000,
    )),
    ("classifier", LogisticRegression(
        max_iter=2000,
        class_weight="balanced",
        random_state=42,
    )),
])

# --------------------------------------------------
# 5. Train model
# --------------------------------------------------

print("\nTraining model...")

model.fit(X_train, y_train)

print("Training completed!")

# --------------------------------------------------
# 6. Validation evaluation
# --------------------------------------------------

val_predictions = model.predict(X_val)

print("\nVALIDATION RESULTS")
print("------------------")
print("Accuracy:", accuracy_score(y_val, val_predictions))
print("F1-score:", f1_score(y_val, val_predictions))

print("\nClassification Report:")
print(classification_report(
    y_val,
    val_predictions,
    target_names=["Not Food Safety", "Food Safety"],
    zero_division=0,
))

print("\nConfusion Matrix:")
print(confusion_matrix(y_val, val_predictions))

# --------------------------------------------------
# 7. Retrain on training + validation
# --------------------------------------------------

X_final = pd.concat([X_train, X_val])
y_final = pd.concat([y_train, y_val])

model.fit(X_final, y_final)

# --------------------------------------------------
# 8. Final held-out test evaluation
# --------------------------------------------------

test_predictions = model.predict(X_test)

print("\nFINAL TEST RESULTS")
print("------------------")
print("Accuracy:", accuracy_score(y_test, test_predictions))
print("F1-score:", f1_score(y_test, test_predictions))

print("\nClassification Report:")
print(classification_report(
    y_test,
    test_predictions,
    target_names=["Not Food Safety", "Food Safety"],
    zero_division=0,
))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, test_predictions))

# --------------------------------------------------
# 9. Save trained model
# --------------------------------------------------

joblib.dump(model, MODEL_PATH)

print("\nModel saved successfully!")
print("Location:", MODEL_PATH)
