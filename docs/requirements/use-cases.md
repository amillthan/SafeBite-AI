# SafeBite AI — Use Cases and Acceptance Criteria

**Version:** 0.1.0

**Status:** Draft

## 1. Actors

### Analyst
Submits restaurant reviews, examines AI predictions, investigates complaint patterns, and reviews alerts.

### Administrator
Manages system configuration and oversees alert review.

These are planned roles. Authentication and role-based permissions will be implemented separately.

---

## 2. Use Cases

### UC-01: Analyze a Restaurant Review

**Actor:** Analyst  
**Related requirements:** FR-01, FR-02, FR-03

**Preconditions:**
- The application is running.
- A trained classification model is available.

**Main flow:**
1. The analyst opens the dashboard.
2. The analyst enters a restaurant review.
3. The system validates the input.
4. The system preprocesses the review.
5. The ML model predicts whether the review contains a potential food safety concern.
6. The dashboard displays the result.

**Alternative flow:**
- If the review text is empty, the system displays a validation error.

**Acceptance criteria:**
- Valid review text is accepted.
- Empty review text is rejected.
- A prediction is returned when the model is available.
- The result is clearly identified as an AI prediction, not a verified fact.

### UC-02: Identify Food Safety Complaint Categories

**Actor:** Analyst  
**Related requirement:** FR-04

**Main flow:**
1. The analyst submits a review.
2. The system identifies possible complaint categories.
3. The dashboard displays the identified categories.

**Acceptance criteria:**
- The system supports all seven complaint categories defined in the SRS.
- A review may receive multiple categories.
- Reviews without identified safety concerns are not forced into a complaint category.

### UC-03: Detect Similar Complaints

**Actor:** Analyst  
**Related requirement:** FR-05

**Main flow:**
1. The analyst selects a restaurant or review collection.
2. The system compares the review texts.
3. The system identifies potentially similar complaints.
4. The analyst examines the matched reviews.

**Acceptance criteria:**
- Similarity results identify the related review records.
- The analyst can inspect the original review texts.
- Similar complaints are not automatically treated as separate verified incidents.

### UC-04: Monitor Restaurant Complaint Trends

**Actor:** Analyst  
**Related requirement:** FR-06

**Main flow:**
1. The analyst selects a restaurant.
2. The system retrieves available review records.
3. The system groups relevant complaints by date.
4. The dashboard displays complaint trends.

**Acceptance criteria:**
- Trend analysis uses the correct restaurant records.
- Time-based analysis uses available review dates.
- Missing dates are handled appropriately.
- Charts distinguish reported complaints from verified incidents.

### UC-05: Review an Early Warning Alert

**Actor:** Analyst or Administrator  
**Related requirement:** FR-07

**Main flow:**
1. The system identifies a complaint pattern that meets a configured alert condition.
2. The system creates an internal alert.
3. An authorized user opens the alert.
4. The user reviews the supporting complaints.
5. The user records a review decision.

**Acceptance criteria:**
- Alerts are generated only when configured conditions are met.
- Alerts contain supporting information.
- Alerts remain internal.
- The system records the review status.
- The system does not automatically declare a restaurant unsafe.

### UC-06: View the Dashboard

**Actor:** Analyst  
**Related requirement:** FR-08

**Main flow:**
1. The analyst opens the Streamlit dashboard.
2. The dashboard displays available analysis features.
3. The analyst selects a feature.
4. The dashboard displays the requested information.

**Acceptance criteria:**
- The dashboard provides access to review analysis.
- Classification results are readable.
- Complaint trends and alerts are clearly presented when data is available.
- Application errors are explained using understandable messages.

### UC-07: Store and Retrieve Analysis Records

**Actor:** System  
**Related requirement:** FR-09

**Main flow:**
1. The system receives a valid review record.
2. The system stores the review information.
3. The system stores the corresponding analysis result.
4. The system retrieves records when requested by an authorized application component.

**Acceptance criteria:**
- Review records can be stored and retrieved.
- Analysis results are associated with the correct reviews.
- Restaurant relationships remain consistent.
- Database errors are handled appropriately.

---

## 3. General Acceptance Criteria

SafeBite AI should meet the following conditions before its first release:

- Core application features pass their functional tests.
- The food safety classifier is evaluated using precision, recall, F1-score, and a confusion matrix.
- Model evaluation avoids training-data leakage.
- Invalid inputs are handled safely.
- Sensitive configuration values are not committed to GitHub.
- Internal alerts require human review.
- The dashboard clearly communicates model limitations.
- The application does not treat unverified reviews as confirmed food safety violations.

---

## 4. Document Status

These use cases and acceptance criteria describe the intended behavior of SafeBite AI.

They will guide implementation, testing, and future requirements refinement.