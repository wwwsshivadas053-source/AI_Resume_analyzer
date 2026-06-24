import re

KEYWORDS = [
    "python",
    "sql",
    "machine learning",
    "data analysis",
    "flask",
    "django",
    "aws",
    "power bi",
    "excel",
    "javascript",
    "html",
    "css",
    "git",
    "github"
]

def calculate_ats_score(text):

    score = 0

    text = text.lower()

    for keyword in KEYWORDS:

        if keyword in text:
            score += 7

    score = min(score, 100)

    return score