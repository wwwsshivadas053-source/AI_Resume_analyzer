
# resume_ai.py

# ==========================================================
# GEMINI CONFIGURATION (NO .ENV REQUIRED)
# ==========================================================

GEMINI_API_KEY = "AQ.Ab8RN6J4K7Df_l8_l66r1Yrkwp_Hn__-JS50xr-koUgHChJAJQ"

model = None

try:
    import google.generativeai as genai

    genai.configure(api_key=GEMINI_API_KEY)

    # Recommended model
    model = genai.GenerativeModel("gemini-1.5-flash")

except Exception as e:
    print("Gemini initialization failed:", e)
    model = None


# ==========================================================
# LOCAL FALLBACK ANALYSIS
# ==========================================================

def _local_resume_analysis(text):
    lowered = text.lower()

    strengths = []
    weaknesses = []
    missing = []

    if len(text.split()) >= 350:
        strengths.append(
            "Resume has sufficient content for ATS parsing."
        )
    else:
        weaknesses.append(
            "Resume is short. Add more project and experience details."
        )

    keywords = [
        "python",
        "sql",
        "flask",
        "machine learning",
        "javascript",
        "aws",
        "html",
        "css",
        "git",
        "github"
    ]

    for keyword in keywords:
        if keyword in lowered:
            strengths.append(
                f"Includes keyword: {keyword}"
            )
        else:
            missing.append(keyword)

    if not any(char.isdigit() for char in text):
        weaknesses.append(
            "Add quantified achievements and measurable results."
        )

    suggestions = [
        "Add a professional summary.",
        "Use action verbs in experience section.",
        "Include measurable achievements.",
        "Tailor keywords to target job description.",
        "Organize skills by category."
    ]

    ats_score = max(
        40,
        min(
            95,
            60
            + len(strengths) * 3
            - len(weaknesses) * 2
        )
    )

    report = f"""
ATS Score: {ats_score}/100

Strengths:
"""

    for item in strengths[:6]:
        report += f"\n• {item}"

    report += "\n\nWeaknesses:"

    for item in weaknesses[:6]:
        report += f"\n• {item}"

    report += "\n\nMissing Skills:"

    if missing:
        for item in missing[:10]:
            report += f"\n• {item}"
    else:
        report += "\n• No major missing keywords found."

    report += "\n\nSuggestions:"

    for item in suggestions:
        report += f"\n• {item}"

    return report


# ==========================================================
# ATS ANALYZER
# ==========================================================

def analyze_resume(text):

    if not text.strip():
        return "Resume text is empty."

    if not model:
        return _local_resume_analysis(text)

    prompt = f"""
You are a senior ATS recruiter.

Analyze the following resume.

Return ONLY:

ATS Score: X/100

Strengths:
- ...

Weaknesses:
- ...

Missing Skills:
- ...

Suggestions:
- ...

Resume:

{text}
"""

    try:
        response = model.generate_content(prompt)

        if hasattr(response, "text"):
            return response.text

        return _local_resume_analysis(text)

    except Exception as exc:

        return (
            _local_resume_analysis(text)
            + f"\n\nGemini note: {exc}"
        )


# ==========================================================
# RESUME REWRITER
# ==========================================================

def rewrite_resume(text):

    if not text.strip():
        return "Resume text is empty."

    if not model:
        return (
            "Gemini API not available.\n\n"
            "Resume Content:\n\n"
            + text
        )

    prompt = f"""
You are a professional resume writer.

Rewrite this resume to improve:

1. ATS Score
2. Grammar
3. Professional Summary
4. Skills Section
5. Project Descriptions
6. Experience Section

Keep all original information.

Resume:

{text}
"""

    try:

        response = model.generate_content(prompt)

        if hasattr(response, "text"):
            return response.text

        return "Resume rewrite failed."

    except Exception as exc:
        return f"Rewrite failed: {exc}"


# ==========================================================
# TESTING
# ==========================================================

if __name__ == "__main__":

    sample_resume = """
    Prajwal T S

    Python Developer

    Skills:
    Python, Flask, HTML, CSS, JavaScript, SQL

    Projects:
    Disease Prediction System
    Resume Analyzer
    College Notes RAG Chatbot
    """

    print(analyze_resume(sample_resume))

