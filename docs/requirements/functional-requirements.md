# SafeBite AI — Functional Requirements

**Version:** 0.1.0

**Status:** Draft

## 1. Review Submission

**Requirement ID:** FR-01

The system shall allow analysts to submit restaurant reviews for food safety analysis.

**Inputs:**
- Review text (required)
- Restaurant identifier (optional for single-review analysis)
- Review date (optional)

**Expected behavior:**
- Validate that the review text is not empty.
- Accept valid review text for analysis.
- Display an appropriate error message for invalid input.

## 2. Review Preprocessing

**Requirement ID:** FR-02

The system shall prepare review text before passing it to the machine learning model.

**Expected behavior:**
- Normalize text using the preprocessing steps required by the selected model.
- Handle missing or invalid text.
- Apply the same fitted preprocessing pipeline during training and prediction.

## 3. Food Safety Classification

**Requirement ID:** FR-03

The system shall classify each review into one of two categories:

- Potential food safety concern
- No identified food safety concern

**Expected behavior:**
- Receive valid review text.
- Apply the trained classification model.
- Return the predicted category.
- Return a model score when supported and appropriately validated.

## 4. Complaint Categorization

**Requirement ID:** FR-04

The system shall identify potential complaint categories.

**Categories:**
- Suspected foodborne illness
- Undercooked food
- Spoiled or contaminated food
- Poor hygiene
- Pest-related complaints
- Foreign objects in food
- Allergen-related concerns

A single review may contain multiple complaint categories.

## 5. Similar Complaint Detection

**Requirement ID:** FR-05

The system shall identify reviews that may describe similar complaints.

**Expected behavior:**
- Compare reviews using text similarity techniques.
- Identify potential duplicates or related complaints.
- Allow analysts to inspect the matched reviews.
- Avoid automatically treating similar reviews as independent incidents.

## 6. Restaurant Trend Monitoring

**Requirement ID:** FR-06

The system shall monitor patterns of reported food safety concerns for individual restaurants.

**Expected behavior:**
- Group review records by restaurant.
- Analyze reports over time when dates are available.
- Display changes in the number or proportion of concerning reviews.
- Clearly distinguish review counts from verified food safety incidents.

## 7. Early Warning Alerts

**Requirement ID:** FR-07

The system shall generate internal alerts when predefined complaint patterns or thresholds are detected.

**Expected behavior:**
- Evaluate restaurant-level complaint patterns.
- Generate an alert when configured conditions are met.
- Display supporting review information.
- Allow human review before further action.
- Avoid automatically publishing accusations or unsafe-restaurant labels.

## 8. Dashboard

**Requirement ID:** FR-08

The system shall provide a Streamlit dashboard.

**Expected behavior:**
- Allow review submission.
- Display classification results.
- Display complaint categories.
- Show restaurant-level trends.
- Display alerts for human review.

## 9. Data Storage

**Requirement ID:** FR-09

The system shall store relevant application records in PostgreSQL.

**Expected behavior:**
- Store restaurant information.
- Store review records.
- Store analysis results.
- Store generated alerts and their review status.
- Maintain relationships between records.

## 10. Responsible AI Requirements

The system shall treat customer reviews as unverified reports.

The system must not present a model prediction as proof of a food safety violation, confirmed illness, or restaurant responsibility.

Any alerts must remain internal and subject to human review.