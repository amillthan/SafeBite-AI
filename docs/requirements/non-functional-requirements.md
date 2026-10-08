# SafeBite AI — Non-Functional Requirements

**Version:** 0.1.0  
**Status:** Draft

## 1. Performance Requirements

### NFR-01: Prediction Response Time

The system should return a classification result for a single restaurant review within 3 seconds under normal operating conditions, after the model has loaded.

### NFR-02: API Response Time

The backend should respond to basic API requests within 1 second under normal operating conditions.

### NFR-03: Dataset Processing

The system should support processing multiple reviews in batches without exhausting available system memory.

Performance targets will be tested and refined based on the development environment.

## 2. Security Requirements

### NFR-04: Environment Configuration

Sensitive configuration values, including database credentials and API secrets, shall be stored in environment variables rather than directly in source code.

### NFR-05: Input Validation

The backend shall validate user inputs and reject invalid requests with appropriate error messages.

### NFR-06: Database Security

Database access shall use parameterized queries or an ORM to reduce SQL injection risks.

### NFR-07: Access Control

Private alert information shall be accessible only to authorized users when authentication and authorization are implemented.

Until access control is implemented, the application must not expose private alerts through a publicly accessible deployment.

## 3. Reliability Requirements

### NFR-08: Error Handling

The system shall handle invalid inputs, unavailable models, and database connection failures without unexpected application crashes.

### NFR-09: Data Integrity

The system shall maintain consistent relationships between restaurants, reviews, predictions, and alerts.

### NFR-10: Logging

The backend shall record important application events and errors without exposing credentials or unnecessary sensitive review information.

## 4. Maintainability Requirements

### NFR-11: Modular Architecture

The application shall separate its major components into:

- Streamlit frontend
- FastAPI backend
- Machine learning package
- PostgreSQL database

### NFR-12: Code Quality

Python code shall follow consistent formatting and linting standards using Ruff.

### NFR-13: Documentation

The project shall maintain documentation covering system requirements, architecture, datasets, APIs, and model evaluation.

### NFR-14: Version Control

Development shall use Git and GitHub with feature branches and Pull Requests.

## 5. Machine Learning Quality Requirements

### NFR-15: Classification Evaluation

The food safety classification model shall be evaluated using precision, recall, F1-score, and a confusion matrix.

### NFR-16: Data Leakage Prevention

Training and evaluation data shall be separated before fitting any data-dependent preprocessing or feature extraction steps.

### NFR-17: Reproducibility

Model training shall use recorded configurations, dataset versions, and random seeds where applicable.

### NFR-18: Model Limitations

The application shall communicate that model predictions are estimates based on review text and may be incorrect.

### NFR-19: Error Analysis

The project shall analyze false positives and false negatives, particularly cases involving possible food safety concerns.

### NFR-20: Model Versioning

Saved model artifacts shall include sufficient metadata to identify their model version, training configuration, and evaluation results.

## 6. Usability Requirements

### NFR-21: User-Friendly Interface

The Streamlit dashboard shall use clear labels, understandable navigation, and readable analysis results.

### NFR-22: Explainable Results

The dashboard should display the predicted category and supporting information that helps analysts interpret the result.

### NFR-23: Clear Error Messages

The application shall provide understandable error messages when users submit invalid data or an operation fails.

## 7. Responsible AI and Privacy Requirements

### NFR-24: Unverified Reports

The application shall clearly identify customer reviews as unverified reports rather than confirmed food safety incidents.

### NFR-25: Human Oversight

Early warning alerts shall require human review before any external reporting or action.

### NFR-26: Privacy Protection

The application shall avoid collecting unnecessary personal information and shall restrict access to stored review data where appropriate.

### NFR-27: Fairness and Bias Evaluation

The project should investigate whether model performance differs across relevant review styles, restaurant groups, or other available and appropriate evaluation subsets.

### NFR-28: Data Source Compliance

The application shall use review datasets and external data sources only where their licenses, permissions, and applicable terms allow the intended use.

## 8. Testing Requirements

### NFR-29: Automated Testing

The project shall include automated tests for important backend functions and machine learning components using Pytest.

### NFR-30: Integration Testing

The project shall test communication between the frontend, backend, ML inference components, and database.

### NFR-31: Regression Testing

Existing tests shall be rerun after significant changes to detect unexpected behavior.

---

## 9. Document Status

This document defines the initial non-functional requirements for SafeBite AI.

Performance targets and other measurable quality requirements will be reviewed during implementation and testing.