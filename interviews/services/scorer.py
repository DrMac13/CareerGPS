import re


ROLE_KEYWORDS = {

    "Software Engineer": [
        "python",
        "django",
        "api",
        "database",
        "sql",
        "javascript",
        "algorithm",
        "debug",
        "testing",
        "backend",
        "frontend",
        "software"
    ],

    "Data Analyst": [
        "sql",
        "excel",
        "power bi",
        "tableau",
        "analysis",
        "data",
        "dashboard",
        "report",
        "cleaning",
        "visualization"
    ],

    "Business Analyst": [
        "stakeholder",
        "requirement",
        "process",
        "business",
        "analysis",
        "workflow",
        "user",
        "solution",
        "project"
    ]
}


def evaluate_response(role, question, response_text):

    score = 0

    strengths = []
    improvements = []

    response_lower = response_text.lower()


    word_count = len(response_text.split())

    if word_count >= 50:
        score += 30
        strengths.append(
            "Provided a detailed response"
        )

    elif word_count >= 25:
        score += 20

    elif word_count >= 10:
        score += 10

    else:
        improvements.append(
            "Provide more detail"
        )

       
    # KEYWORD SCORE (30)
     

    keywords = ROLE_KEYWORDS.get(role, [])

    matches = 0

    for keyword in keywords:

        if keyword in response_lower:
            matches += 1

    keyword_score = min(
        30,
        matches * 5
    )

    score += keyword_score

    if matches > 0:

        strengths.append(
            f"Used {matches} relevant industry terms"
        )

    else:

        improvements.append(
            "Include more role-specific terminology"
        )

     
    # STRUCTURE SCORE (20)
     

    sentences = re.split(
        r"[.!?]+",
        response_text
    )

    valid_sentences = [
        s for s in sentences
        if s.strip()
    ]

    if len(valid_sentences) >= 3:

        score += 20

        strengths.append(
            "Answer is well structured"
        )

    elif len(valid_sentences) >= 2:

        score += 10

    else:

        improvements.append(
            "Use complete sentences"
        )

    # STAR SCORE (20)
    

    star_keywords = [
        "situation",
        "task",
        "action",
        "result",
        "challenge",
        "project",
        "responsibility",
        "achieved"
    ]

    star_matches = 0

    for keyword in star_keywords:

        if keyword in response_lower:
            star_matches += 1

    star_score = min(
        20,
        star_matches * 4
    )

    score += star_score

    if star_matches > 0:

        strengths.append(
            "Evidence of STAR-style storytelling"
        )

    else:

        improvements.append(
            "Use STAR methodology examples"
        )

    score = min(score, 100)

    if not strengths:
        strengths.append(
            "Thank you for submitting a response."
        )

    if not improvements:
        improvements.append(
            "Excellent response."
        )

    return {
        "overall_score": score,
        "confidence_score": score,
        "star_score": star_score,
        "strengths": strengths,
        "improvements": improvements
    }