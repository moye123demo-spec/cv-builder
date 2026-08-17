# Profile schema and language policy

Use JSON for deterministic validation. Required top-level fields are name,
headline, location, contact.email, target_role, summary, skills, education,
and experience.

Use dates in YYYY.MM-YYYY.MM, YYYY.MM-present, or YYYY.MM-至今 format. Store
separate employers or appointments as separate experience records.

For English templates, provide verified English strings in a separate profile
file. The generator changes layout labels only; it deliberately does not
machine-translate achievements, publication status, job titles, or metrics.

Academic templates optionally accept research_interests, publications, funding,
and teaching_service. Each may contain strings or records with title, details,
and bullets.
