# SafeBite AI

**AI-Powered Food Safety Early Warning System**

SafeBite AI is an experimental application that analyzes restaurant reviews to identify potential food safety complaints and review-based warning signals.

## Features

- Single restaurant review analysis
- Binary machine learning classification
- Multi-label food safety category detection
- Basic negation handling
- Batch CSV review analysis
- Analytics dashboard
- Experimental early-warning indicators
- Restaurant-level review summaries
- Downloadable CSV analysis results

## Technology Stack

- **Backend:** Python, FastAPI
- **Frontend:** Streamlit
- **Machine Learning:** Scikit-learn, TF-IDF, Logistic Regression
- **Data Processing:** Pandas
- **Testing:** Pytest
- **Code Quality:** Ruff

## Installation

Requires Python 3.11 or another compatible version specified in `pyproject.toml`.

```powershell
git clone https://github.com/amillthan/SafeBite-AI.git
cd SafeBite-AI

python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install -e ".[dev]"
```

## Generate Prototype Model

```powershell
python data/scripts/create_synthetic_dataset.py
python ml/train_baseline.py
```

## Run the Application

Backend:

```powershell
python -m uvicorn backend.app.main:app --reload
```

Frontend (in a separate terminal):

```powershell
python -m streamlit run frontend/app.py
```

Streamlit: http://localhost:8501

FastAPI documentation: http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/predict` | Analyze one restaurant review |
| POST | `/api/predict/batch` | Analyze multiple restaurant reviews |

## Batch CSV Format

The CSV must contain a `text` column.

An optional `restaurant_id` column enables restaurant-level grouping.

Example:

```csv
restaurant_id,text
R001,"The kitchen was filthy."
R001,"I saw cockroaches."
R002,"The food was delicious."
```

## Testing

```powershell
python -m pytest -v
python -m ruff check backend frontend ml tests
```

## Limitations

- The ML model is trained on a small synthetic dataset and is not validated for real-world food safety decisions.
- Keyword-based category detection may produce false positives and false negatives.
- Warning thresholds are experimental and not scientifically validated.
- Review allegations are not verified incidents.
- Yelp Open Dataset usage remains subject to licensing clarification.
- This prototype is intended for development, demonstration, and research exploration only.
