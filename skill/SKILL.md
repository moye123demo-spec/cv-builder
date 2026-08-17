---
name: cv-builder
description: Generate, edit, tailor, translate, or quality-check professional resumes/CVs for Chinese or English job applications. Use when a user provides career information, an existing resume, a job description, or requests an ATS-safe DOCX/PDF resume, including industry, academic, biotech, healthcare, AI, data, and research-to-industry applications.
---

# CV Builder

## Workflow

1. Collect verified facts in the profile schema. Do not infer missing dates,
   employers, degrees, publications, skills, metrics, or titles.
2. Read `references/content_rules.md` before drafting. Read
   `references/role_profiles.md` when tailoring to a target role.
3. Read references/input_schema.md for bilingual or academic inputs. Validate
   the profile with scripts/validate_profile.py.
4. Run scripts/match_jd.py when a job description is available. Its percentage
   is rule-based keyword and alias evidence coverage, not a hiring prediction.
   Treat the report as prioritization evidence, never as permission to add new claims.
5. Draft a role-specific resume. Prioritize relevant evidence, outcomes,
   technical scope, and transferable value; preserve factual ownership.
6. Generate an editable DOCX with scripts/generate_resume.py and an explicit
   template choice. Use the
   `documents` skill when layout or DOCX editing is needed.
7. Export PDF when requested and use the `pdf` skill plus
   `scripts/qa_pdf.py` to render and inspect every page.
8. Deliver the requested files and state any remaining placeholders or
   unverified facts.

## Rules

- Separate confirmed facts from proposed wording. Never transform a submitted,
  revised, or in-preparation manuscript into a published paper.
- Keep employment dates, institutions, and accomplishments attached to the
  correct role. If a user has consecutive roles, list them separately.
- Use an ATS-safe single-column layout unless the user explicitly asks for a
  visual template. Use tables only for compact contact/header layout.
- Omit sensitive personal data by default. Add a photo, date of birth,
  government ID, marital status, or home address only on explicit request.
- Keep GitHub examples anonymous. Never add the user's real CV, image, email,
  phone number, unpublished work, or private files to the repository.

## Inputs and resources

- Start from `assets/profiles/ai_biomed_anonymized.json` for the JSON shape.
- Use `scripts/validate_profile.py` for required-field and date checks.
- Use template values industry-cn, original-cn, ats-cn, academic-cn,
  industry-en, or academic-en with scripts/generate_resume.py.
- Template behavior comes from assets/styles/*.json; modify a style file to
  change colors, margins, language, photo behavior, or bilingual headings.
- Use scripts/export_pdf.py with auto, libreoffice, or word engine when a
  PDF is required. Auto tries LibreOffice first and Microsoft Word on Windows.
- Use scripts/match_jd.py for an auditable JD matching report.
- Use `scripts/qa_pdf.py` after PDF export to confirm key text and page
  count. Visual inspection remains mandatory for final delivery.

## Output checklist

- Correct target role, employer names, date ranges, and publication status.
- Clear contact line and functional links, without overflow.
- Education and strongest technical capabilities visible on page one.
- No placeholders, fabricated claims, clipped text, overlapping elements, or
  isolated headings at page bottoms.
