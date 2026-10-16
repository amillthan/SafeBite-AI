
# SafeBite AI

**AI-Powered Food Safety Early Warning System**

SafeBite AI is an experimental machine learning application that analyzes restaurant customer reviews to identify potential food safety complaints and generate review-based early warning indicators.

The application uses a binary machine learning classifier trained on 501 manually labeled restaurant reviews.

## Features

- Single restaurant review analysis
- Binary machine learning classification
- Rule-based food safety category detection
- Basic negation handling
- Batch CSV review analysis
- Food safety analytics dashboard
- Experimental early warning indicators
- Restaurant-level review summaries
- Downloadable CSV analysis results

## Technology Stack

- **Backend:** Python, FastAPI
- **Frontend:** Streamlit
- **Machine Learning:** Scikit-learn, TF-IDF, Logistic Regression
- **Data Processing:** Pandas, NumPy
- **Model Storage:** Joblib
- **Testing:** Pytest
- **Code Quality:** Ruff

## Machine Learning Model

The model was trained using 501 manually labeled restaurant reviews from the BDFoodSent dataset.

### Classification Labels

- **1:** Potential Food Safety Complaint
- **0:** No Food Safety Complaint

### Model Architecture

- Text feature extraction: TF-IDF
- N-gram range: Unigrams and bigrams
- Classification algorithm: Logistic Regression
- Class balancing: Balanced class weights
- Data splitting: Stratified train, validation, and test sets

### Model Evaluation

The final model was evaluated on a held-out test set containing 76 reviews.

| Metric | Result |
|---|---|
| Test Accuracy | 84.21% |
| Food Safety Precision | 79.59% |
| Food Safety Recall | 95.12% |
| Food Safety F1-Score | 86.67% |

These results reflect performance on a small, keyword-enriched evaluation dataset and may not generalize to real-world restaurant reviews.

### Model Files

- **Trained model:** `models/safebite_binary_model.joblib`
- **Training script:** `training/train_model.py`
- **Model testing script:** `training/test_model.py`
- **Labeled dataset:** `data/annotations/SafeBite_AI_labeled_501.csv`

The trained model and labeled review dataset are maintained locally and are not included in the public Git repository.

## Food Safety Categories

SafeBite AI uses rule-based keyword detection to identify six food safety categories:

1. Hygiene
2. Food Contamination
3. Undercooked Food
4. Suspected Illness
5. Pest Activity
6. Food Storage

These categories are identified using predefined rules, not a separate multi-class machine learning model.

Category detection is applied to reviews classified as potential food safety complaints.

## Installation

### Requirements

- Python 3.11 or a compatible version
- Git
- pip

### Clone the Repository

```powershell
git clone https://github.com/amillthan/SafeBite-AI.git
cd SafeBite-AI
```

### Create a Virtual Environment

```powershell
python -m venv .venv
```

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Install Dependencies

```powershell
python -m pip install -e ".[dev]"
```

## Model Setup

Before running the application, ensure that the trained model is available at:

```text
models/safebite_binary_model.joblib
```

The trained model is not distributed through the public Git repository.

The application does not automatically generate a synthetic model.

If the model file is missing, restore the existing trained model before starting the backend.

## Run the Application

### Start the Backend

Open a terminal in the project root:

```powershell
.\run_backend.ps1
```

Alternatively:

```powershell
python -m uvicorn backend.app.main:app --reload
```

Backend URL:

http://127.0.0.1:8000

Swagger API documentation:

http://127.0.0.1:8000/docs

### Start the Frontend

Open another terminal and activate the virtual environment.

Run:

```powershell
python -m streamlit run frontend/app.py
```

Frontend URL:

http://localhost:8501

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/predict` | Analyze a single restaurant review |
| POST | `/api/predict/batch` | Analyze multiple restaurant reviews |

### Single Review Prediction

Request:

```json
{
  "text": "The chicken was raw and undercooked."
}
```

Example response:

```json
{
  "prediction": 1,
  "label": "Potential Food Safety Complaint",
  "confidence": 0.7341,
  "categories": ["Undercooked Food"]
}
```

The confidence score represents the model's estimated probability for its predicted class. It does not establish whether a complaint is factually correct.

## Batch CSV Analysis

The application supports analyzing multiple restaurant reviews through CSV upload.

The CSV must contain a `text` column.

An optional `restaurant_id` column enables restaurant-level grouping.

Example:

```csv
restaurant_id,text
R001,"The kitchen was filthy."
R001,"I saw cockroaches."
R002,"The food was delicious."
```

The application supports a maximum of 1,000 reviews per batch upload.

### Batch Analysis Results

- Total reviews analyzed
- Number of ML-flagged complaints
- Percentage of flagged complaints
- Prediction distribution
- Food safety category distribution
- Experimental early warning indicators
- Restaurant-level warning summaries
- Downloadable prediction results

## Testing

Run automated tests:

```powershell
python -m pytest -q
```

Run code quality checks:

```powershell
python -m ruff check backend frontend ml tests
```

The existing automated test suite passed all 27 tests during final model integration.

## Project Structure

```text
SafeBite-AI/
|
|-- backend/
|   |-- app/
|       |-- main.py
|       |-- routes/
|       |-- services/
|           |-- prediction_service.py
|           |-- category_service.py
|
|-- frontend/
|   |-- app.py
|   |-- annotation_app.py
|
|-- data/
|   |-- annotations/
|   |-- scripts/
|
|-- training/
|   |-- train_model.py
|   |-- test_model.py
|
|-- models/
|   |-- safebite_binary_model.joblib
|
|-- docs/
|   |-- prediction-api.md
|
|-- tests/
|
|-- run_backend.ps1
|-- requirements.txt
|-- pyproject.toml
|-- README.md
```

The model file and local annotation data may be absent from a fresh public clone.

## Dataset and Usage Permissions

This research prototype uses manually labeled reviews sourced from BDFoodSent.

Clarification regarding dataset redistribution and model-training permissions has been requested from the dataset authors.

Until these permissions are confirmed, the raw review data, manually annotated review data, and trained model are not intended for public redistribution.

## Limitations

- The classifier was trained using only 501 manually labeled restaurant reviews.
- The test dataset is small and keyword-enriched, so the reported performance may not represent real-world results.
- The model may produce false positives and false negatives.
- Food safety categories are detected using predefined rules rather than a separate trained category classifier.
- Early warning thresholds are experimental and have not been scientifically validated.
- Restaurant review allegations are not verified food safety incidents.
- The application is not intended to replace professional food safety inspections.
- Dataset usage and redistribution permissions remain subject to clarification.
- Further evaluation is required before production deployment.

## Project Status

**Version:** Research Prototype V1

Completed components:

- Manual review annotation
- Binary ML model training
- Model evaluation
- FastAPI prediction integration
- Single-review analysis
- Batch review analysis
- Streamlit analytics dashboard
- Automated backend testing

SafeBite AI is intended for academic research, demonstration, and further development.
