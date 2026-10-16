import os

import pandas as pd
import requests
import streamlit as st

API_BASE_URL = os.getenv(
    "SAFEBITE_API_URL",
    "http://127.0.0.1:8000"
).rstrip("/")

API_URL = f"{API_BASE_URL}/api/predict"
BATCH_API_URL = f"{API_BASE_URL}/api/predict/batch"

st.set_page_config(
    page_title="SafeBite AI",
    page_icon="🍽️",
    layout="wide"
)

st.title("🍽️ SafeBite AI")
st.subheader("AI-Powered Food Safety Early Warning System")

st.write(
    "Analyze restaurant reviews to identify potential "
    "food safety complaints using machine learning."
)

st.divider()

st.header("Food Safety Review Analyzer")

review_text = st.text_area(
    "Enter a restaurant review",
    placeholder="Example: I found a cockroach in my food.",
    height=150,
    max_chars=10000
)

if st.button("Analyze Review", type="primary"):

    if not review_text.strip():
        st.warning("Please enter a restaurant review.")

    else:
        try:
            with st.spinner("Analyzing review..."):
                response = requests.post(
                    API_URL,
                    json={"text": review_text},
                    timeout=30
                )

                response.raise_for_status()
                result = response.json()

            prediction = result["prediction"]
            confidence = result["confidence"]

            st.subheader("Analysis Result")

            if prediction == 1:
                st.warning(
                    "Potential Food Safety Complaint Detected"
                )
            else:
                st.success(
                    "No Food Safety Complaint Detected"
                )

            st.metric(
                "Model Confidence",
                f"{confidence * 100:.2f}%"
            )

            categories = result.get("categories", [])

            st.subheader("Detected Food Safety Categories")

            if categories:
                for category in categories:
                    st.write(f"• {category}")

                if prediction == 0:
                    st.warning(
                        "The ML model classified this review as normal, "
                        "but keyword-based detection identified potential "
                        "food safety concerns. This result requires review."
                    )
            else:
                st.info("No specific food safety categories identified.")

            st.caption(
                "This is an experimental AI prediction, "
                "not a verified food safety finding."
            )

        except requests.exceptions.RequestException:
            st.error(
                "Unable to connect to the SafeBite AI backend. "
                "Please check whether the FastAPI server is running."
            )
        except (ValueError, KeyError, TypeError):
            st.error("The backend returned an unexpected response.")

st.divider()

st.info(
    "Research Prototype: This model was trained using "
    "501 manually labeled restaurant reviews. "
    "Predictions are experimental and should not be "
    "treated as verified food safety findings."
)

st.divider()
st.header("Batch Review Analysis")

uploaded_file = st.file_uploader(
    "Upload a CSV file containing restaurant reviews",
    type=["csv"],
)

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        if "text" not in df.columns:
            st.error("CSV must contain a column named 'text'.")

        else:
            st.write(f"Total rows: {len(df)}")

            if st.button("Analyze CSV Reviews"):
                if df.empty:
                    st.warning("The uploaded CSV contains no reviews.")

                elif len(df) > 1000:
                    st.warning("Maximum 1000 reviews per upload.")

                elif df["text"].isna().any():
                    st.error("The text column contains missing reviews.")

                else:
                    reviews = df["text"].astype(str).tolist()

                    if (
                        "restaurant_id" in df.columns
                        and (
                            df["restaurant_id"].isna().any()
                            or df["restaurant_id"].astype(str).str.strip().eq("").any()
                        )
                    ):
                        st.error("Restaurant IDs must not be empty.")
                        st.stop()

                    with st.spinner("Analyzing reviews..."):
                        response = requests.post(
                            BATCH_API_URL,
                            json={
                                "reviews": reviews,
                                "restaurant_ids": (
                                    df["restaurant_id"].astype(str).tolist()
                                    if "restaurant_id" in df.columns
                                    else None
                                ),
                            },
                            timeout=180,
                        )

                        response.raise_for_status()
                        response_data = response.json()

                        results = response_data["results"]
                        warning = response_data["warning"]
                        restaurant_summaries = response_data.get("restaurants", [])

                    results_df = pd.DataFrame(results)

                    st.divider()
                    st.header("Food Safety Analytics Dashboard")

                    total_reviews = len(results_df)
                    complaint_count = int((results_df["prediction"] == 1).sum())
                    complaint_percentage = (
                        complaint_count / total_reviews * 100
                        if total_reviews > 0 else 0
                    )

                    disagreement_count = int(
                        (
                            (results_df["prediction"] == 0)
                            & results_df["categories"].apply(bool)
                        ).sum()
                    )

                    col1, col2, col3, col4 = st.columns(4)

                    col1.metric("Total Reviews", total_reviews)
                    col2.metric("ML-Flagged Complaints", complaint_count)
                    col3.metric("ML Complaint Rate", f"{complaint_percentage:.1f}%")
                    col4.metric("ML/Keyword Disagreements", disagreement_count)

                    st.subheader("Prediction Distribution")

                    prediction_counts = (
                        results_df["label"]
                        .value_counts()
                    )

                    st.bar_chart(prediction_counts)

                    st.subheader("Food Safety Category Distribution")

                    category_counts = results_df["categories"].explode()

                    category_counts = category_counts[
                        category_counts.notna() & (category_counts != "")
                    ].value_counts()

                    if not category_counts.empty:
                        st.bar_chart(category_counts)
                    else:
                        st.info("No food safety categories detected.")

                    results_df["categories"] = results_df[
                        "categories"
                    ].apply(lambda values: ", ".join(values))

                    st.success("Batch analysis completed!")

                    st.dataframe(
                        results_df,
                        width="stretch",
                    )

                    st.download_button(
                        label="Download Analysis Results",
                        data=results_df.to_csv(index=False),
                        file_name="safebite_analysis_results.csv",
                        mime="text/csv",
                    )

                    st.divider()
                    st.header("Early Warning Indicators")

                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "Flagged Reviews",
                        warning["flagged_reviews"],
                    )

                    col2.metric(
                        "Flagged Review Rate",
                        f'{warning["complaint_rate"]:.2f}%',
                    )

                    col3.metric(
                        "Warning Level",
                        warning["warning_level"],
                    )

                    st.caption(
                        "Experimental indicators based on review text. "
                        "They do not establish actual food safety conditions."
                    )

                    if restaurant_summaries:
                        st.divider()
                        st.header("Restaurant-Level Warning Summary")

                        restaurant_df = pd.DataFrame(restaurant_summaries)

                        st.dataframe(
                            restaurant_df,
                            width="stretch",
                        )

                        st.caption(
                            "Restaurant warning levels are experimental "
                            "review-based indicators, not verified safety ratings."
                        )

    except pd.errors.ParserError:
        st.error("Invalid CSV format.")
    except requests.exceptions.RequestException as exc:
        st.error(f"Batch analysis request failed: {exc}")