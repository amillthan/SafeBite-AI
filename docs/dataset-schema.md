# SafeBite AI — Dataset Schema

## Dataset Source
Yelp Open Dataset (JSON format)

## Dataset Files
- `yelp_academic_dataset_business.json` — approximately 0.11 GB
- `yelp_academic_dataset_review.json` — approximately 4.98 GB

## Business Fields
- `business_id` — unique business identifier
- `name` — business name
- `categories` — business categories
- `city` — city
- `state` — state

## Review Fields
- `review_id` — unique review identifier
- `business_id` — associated business identifier
- `text` — customer review text
- `date` — review date
- `stars` — customer rating

## Relationship
The `business_id` field connects the business dataset with the review dataset.

## Planned Data Processing
1. Identify restaurant businesses.
2. Select reviews associated with restaurants.
3. Prepare candidate food safety complaints for human annotation, subject to dataset usage permissions.
4. Create a labeled training dataset if permitted.
5. Train and evaluate the food safety classification model.

## Dataset Limitations
- The dataset does not provide food safety classification labels.
- Customer reviews are unverified statements.
- Yelp dataset usage restrictions apply.
- The raw dataset must not be committed to the public GitHub repository.
- Manual annotation and training on Yelp review text are pending clarification of the dataset agreement.

## Data Privacy
Only the minimum fields needed for the academic project should be processed. User identifiers and unnecessary personal information should be excluded.