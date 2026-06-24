import os


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY","")
HAS_REAL_GEMINI_KEY = GEMINI_API_KEY and GEMINI_API_KEY != YOUR_GEMINI_API_KEY

if HAS_REAL_GEMINI_KEY:
    import google.generativeai as genai

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")
else:
    model = None


def _local_resume_analysis(text):
    lowered = text.lower()
    strengths = []
    weaknesses = []
    missing = []

    if len(text.split()) >= 350:
        strengths.append("Resume has enough detail for ATS parsing.")
    else:
        weaknesses.append("Resume looks short; add measurable project and work details.")

    for keyword in ["python", "sql", "flask", "machine learning", "javascript", "aws"]:
        if keyword in lowered:
            strengths.append(f"Includes relevant keyword: {keyword}.")
        else:
            missing.append(keyword)

    if not any(char.isdigit() for char in text):
        weaknesses.append("Add quantified achievements such as percentages, revenue, users, or time saved.")

    if not strengths:
        strengths.append("Readable resume text was extracted successfully.")

    if not weaknesses:
        weaknesses.append("Improve role targeting by mirroring high-value job description keywords.")

    suggestions = [
        "Add a concise professional summary aligned to the target role.",
        "Use action verbs and measurable outcomes in every experience bullet.",
        "Group skills by category so ATS systems can parse them cleanly.",
        "Include role-specific keywords from the job description naturally."
    ]

    return "\n".join([
        "Strengths:",
        *[f"- {item}" for item in strengths[:5]],
        "",
        "Weaknesses:",
        *[f"- {item}" for item in weaknesses[:5]],
        "",
        "Missing Skills:",
        *[f"- {item}" for item in missing[:8]],
        "",
        "Suggestions:",
        *[f"- {item}" for item in suggestions],
    ])

def analyze_resume(text):
    if not model:
        return _local_resume_analysis(text)

    prompt = f"""
You are a professional ATS recruiter.

Analyze this resume.

Return:

ATS Score:
Strengths:
Weaknesses:
Missing Skills:
Suggestions:

Resume:

{text}
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as exc:
        return f"{_local_resume_analysis(text)}\n\nGemini note: {exc}"

def rewrite_resume(text):
    if not model:
        return "Add a real GEMINI_API_KEY in .env to use AI resume rewriting.\n\n" + text

    prompt = f"""
Rewrite this resume professionally.

Improve:

- ATS Score
- Grammar
- Professional Summary
- Skills
- Experience

Resume:

{text}
"""

    response = model.generate_content(
        prompt
    )

    return response.text
