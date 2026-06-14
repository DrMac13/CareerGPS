import re

from pypdf import PdfReader
from docx import Document

from profiles.models import (
    Skill,
    UserSkill,
    UserEducation
)


def extract_text_from_txt(file):

    file.seek(0)

    content = file.read()

    if isinstance(content, bytes):
        return content.decode(
            "utf-8",
            errors="ignore"
        )

    return content


def extract_text_from_pdf(file):

    file.seek(0)

    reader = PdfReader(file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text() or ""
        text += page_text + "\n"

    return text


def extract_text_from_docx(file):

    file.seek(0)

    document = Document(file)

    paragraphs = [
        paragraph.text
        for paragraph in document.paragraphs
    ]

    return "\n".join(paragraphs)


def extract_cv_text(file):

    filename = getattr(file, "name", "").lower()

    if ".txt" in filename:
        return extract_text_from_txt(file)

    if ".pdf" in filename:
        return extract_text_from_pdf(file)

    if ".docx" in filename:
        return extract_text_from_docx(file)

    return ""


def extract_skills_from_text(text):

    matched_skills = []

    all_skills = Skill.objects.all()

    text_lower = text.lower()

    for skill in all_skills:

        skill_name = skill.name.lower()

        pattern = r"\b" + re.escape(skill_name) + r"\b"

        if re.search(pattern, text_lower):
            matched_skills.append(skill)

    return matched_skills


def save_skills_to_profile(profile, skills):

    saved_skills = []

    for skill in skills:

        user_skill, created = UserSkill.objects.get_or_create(
            profile=profile,
            skill=skill,
            defaults={
                "proficiency_level": "Beginner",
                "years_experience": 0
            }
        )

        saved_skills.append(user_skill)

    return saved_skills


def extract_education_from_text(text):

    education_entries = []

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    education_keywords = [
        "university",
        "college",
        "institution",
        "bachelor",
        "bsc",
        "ba",
        "diploma",
        "degree",
        "certificate",
        "honours",
        "masters",
        "phd"
    ]

    for line in lines:

        line_lower = line.lower()

        if any(keyword in line_lower for keyword in education_keywords):

            education_entries.append({
                "institution_name": line,
                "qualification_name": line,
                "field_of_study": "",
                "start_year": None,
                "end_year": None,
                "source": "CV"
            })

    return education_entries[:5]


def save_education_to_profile(profile, education_entries):

    saved_entries = []

    for entry in education_entries:

        education, created = UserEducation.objects.get_or_create(
            profile=profile,
            institution_name=entry["institution_name"],
            qualification_name=entry["qualification_name"],
            defaults={
                "field_of_study": entry.get("field_of_study", ""),
                "start_year": entry.get("start_year"),
                "end_year": entry.get("end_year"),
                "source": entry.get("source", "CV")
            }
        )

        saved_entries.append(education)

    return saved_entries


def process_cv_upload(profile, uploaded_file):

    cv_text = extract_cv_text(
        uploaded_file
    )

    profile.cv_file = uploaded_file
    profile.cv_text = cv_text
    profile.save()

    matched_skills = extract_skills_from_text(
        cv_text
    )

    saved_skills = save_skills_to_profile(
        profile,
        matched_skills
    )

    education_entries = extract_education_from_text(
        cv_text
    )

    saved_education = save_education_to_profile(
        profile,
        education_entries
    )

    return {
        "cv_text": cv_text,
        "skills": [
            skill.skill.name
            for skill in saved_skills
        ],
        "education": [
            {
                "institution_name": item.institution_name,
                "qualification_name": item.qualification_name
            }
            for item in saved_education
        ]
    }