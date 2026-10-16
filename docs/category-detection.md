
# Food Safety Complaint Category Detection

## Overview

SafeBite AI identifies potential food safety concerns mentioned in restaurant reviews using rule-based keyword matching.

Category detection operates independently of the binary ML classifier.

## Supported Categories

1. Hygiene
2. Food Contamination
3. Undercooked Food
4. Suspected Foodborne Illness
5. Pest Activity
6. Food Storage

## Implementation

- Service: `backend/app/services/category_service.py`
- API endpoint: `POST /api/predict`
- Frontend: `frontend/app.py`

## Workflow

1. User enters a restaurant review.
2. FastAPI receives the review.
3. The ML classifier predicts whether the review contains a potential complaint.
4. The category detection service independently identifies matching keywords.
5. The API returns the prediction, label, confidence, and categories.
6. Streamlit displays the results and warns when the two detection methods disagree.

## Example

Input:

"The kitchen was filthy and I saw cockroaches."

Detected categories:

- Hygiene
- Pest Activity

## Testing

- Five automated category detection tests.
- Five automated prediction API tests.
- All 10 tests passing.

## Limitations

- Keyword matching may miss alternative wording.
- Negation and context are not understood.
- Multiple categories can be assigned to one review.
- Category matches are not verified food safety incidents.
- The binary ML classifier is trained on a small synthetic dataset and is not reliable for real-world decisions.
