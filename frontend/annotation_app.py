
from pathlib import Path

import pandas as pd
import streamlit as st

CSV_PATH = Path("data/annotations/SafeBite_AI_assisted_annotation_batch.csv")

CATEGORIES = [
    "hygiene",
    "food_contamination",
    "undercooked_food",
    "suspected_illness",
    "pest_activity",
    "food_storage",
]

st.set_page_config(
    page_title="SafeBite AI Annotation",
    page_icon="🍽️",
    layout="wide",
)

st.title("🍽️ SafeBite AI — Review Annotation")


@st.cache_data
def load_data():
    return pd.read_csv(CSV_PATH, keep_default_na=False)


df = load_data()

if "verification_status" not in df.columns:
    df["verification_status"] = "pending"

if "annotation_status" not in df.columns:
    df["annotation_status"] = "pending"

completed_mask = df["annotation_status"] == "completed"
completed_count = int(completed_mask.sum())
total_count = len(df)

st.progress(completed_count / total_count)
st.write(f"Verified: {completed_count} / {total_count}")

pending_indices = df.index[~completed_mask].tolist()

if not pending_indices:
    st.success("All reviews have been verified!")
    st.stop()

if "position" not in st.session_state:
    st.session_state.position = 0

st.session_state.position = min(
    st.session_state.position,
    len(pending_indices) - 1,
)

index = pending_indices[st.session_state.position]
review = df.loc[index]

st.subheader(
    f"Review {st.session_state.position + 1} "
    f"of {len(pending_indices)} pending reviews"
)

st.info(str(review["text"]))

suggested_label = str(review["suggested_label"]).strip()

if suggested_label in ("1", "1.0"):
    default_label = "1"
elif suggested_label in ("0", "0.0"):
    default_label = "0"
else:
    default_label = "Uncertain"

st.write("**AI Suggested Label:**", default_label)
st.write(
    "**AI Suggested Category:**",
    review.get("suggested_category", ""),
)

label_options = ["1", "0", "Uncertain"]

selected_label = st.radio(
    "Choose the correct label",
    label_options,
    index=label_options.index(default_label),
)

selected_category = ""

if selected_label == "1":
    suggested_category = str(
        review.get("suggested_category", "")
    ).strip()

    category_index = (
        CATEGORIES.index(suggested_category)
        if suggested_category in CATEGORIES
        else 0
    )

    selected_category = st.selectbox(
        "Food safety category",
        CATEGORIES,
        index=category_index,
    )

if st.button("Save & Next", type="primary"):
    if selected_label == "Uncertain":
        df.at[index, "verification_status"] = "needs_review"
        df.at[index, "annotation_status"] = "pending"
        df.at[index, "label"] = ""
        df.at[index, "category"] = ""
    else:
        df.at[index, "label"] = selected_label
        df.at[index, "category"] = selected_category
        df.at[index, "verification_status"] = "verified"
        df.at[index, "annotation_status"] = "completed"

    df.to_csv(CSV_PATH, index=False, encoding="utf-8-sig")
    load_data.clear()
    st.rerun()
