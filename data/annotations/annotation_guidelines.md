
# SafeBite AI — Food Safety Annotation Guidelines

## Classification task
Identify whether a review alleges a potential food safety concern.

## Labels
- 1: Potential food safety complaint
- 0: No food safety complaint
- uncertain: Requires manual review

## Label 1
Use when the review mentions:
- Suspected foodborne illness
- Undercooked or raw food when presented as unsafe
- Pests or insects near food
- Poor hygiene or sanitation
- Food contamination
- Unsafe food storage

## Label 0
Use when the review only mentions:
- Taste or food preferences
- Price
- Service
- Waiting time
- Ambience
- Clearly negated safety concerns

## Special rules
- Negative sentiment does not automatically mean food safety.
- Positive reviews can still contain safety complaints.
- Do not treat hypothetical statements as real incidents.
- Do not infer an illness diagnosis from vague symptoms.
- Mark ambiguous cases as uncertain.
- Do not use unreviewed labels for final model training.
