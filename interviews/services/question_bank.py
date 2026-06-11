QUESTION_BANK = {
    "Software Engineer": [
        "Tell me about yourself.",
        "Explain the difference between a list and a tuple in Python.",
        "What is object-oriented programming?",
        "Describe a project you built and the problem it solved.",
        "How do you debug an error in your code?"
    ],

    "Data Analyst": [
        "Tell me about yourself.",
        "What is the difference between SQL WHERE and HAVING?",
        "How would you explain data cleaning?",
        "Describe a time you used data to make a decision.",
        "What tools do you use for data analysis?"
    ],

    "Business Analyst": [
        "Tell me about yourself.",
        "How do you gather business requirements?",
        "What is the difference between a stakeholder and a user?",
        "Describe a time you solved a business problem.",
        "How do you prioritize requirements?"
    ],
}


def get_questions_for_role(role):
    return QUESTION_BANK.get(
        role,
        [
            "Tell me about yourself.",
            "Why are you interested in this role?",
            "Describe a challenge you overcame.",
            "What are your strengths?",
            "Where do you see yourself in five years?"
        ]
    )