import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/api/predict"

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
    "Prototype Notice: The current model was trained using "
    "a small synthetic dataset. Predictions are for "
    "development and testing only."
)