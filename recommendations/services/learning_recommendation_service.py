LEARNING_RESOURCES = {

    "Python": {
        "title": "Python Tutorial",
        "url": "https://docs.python.org/3/tutorial/"
    },

    "SQL": {
        "title": "SQLBolt",
        "url": "https://sqlbolt.com/"
    },

    "Power BI": {
        "title": "Microsoft Learn Power BI",
        "url": "https://learn.microsoft.com/power-bi/"
    },

    "Communication": {
        "title": "Effective Communication Skills",
        "url": "https://www.coursera.org/learn/wharton-communication-skills"
    },

    "Leadership": {
        "title": "Leadership Foundations",
        "url": "https://www.linkedin.com/learning/"
    },

    "Problem solving": {
        "title": "Problem Solving Techniques",
        "url": "https://www.coursera.org/"
    }
}

def get_learning_recommendations(missing_skills):

    recommendations = []

    for skill in missing_skills:

        if skill in LEARNING_RESOURCES:

            resource = LEARNING_RESOURCES[skill]

            recommendations.append({
                "skill": skill,
                "title": resource["title"],
                "url": resource["url"]
            })

    return recommendations