import os

# ==========================================================
# GEMINI CONFIGURATION (ENVIRONMENT VARIABLE)
# ==========================================================

model = None

try:
    import google.generativeai as genai

    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

    if not GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY environment variable not found."
        )

    genai.configure(api_key=GEMINI_API_KEY)

    # Gemini model
    model = genai.GenerativeModel("gemini-1.5-flash")

except Exception as e:
    print(f"Gemini initialization failed: {e}")
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
            strengths.append(f"Includes keyword: {keyword}")
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
        "Tailor keywords to the target job description.",
        "Organize skills into categories."
    ]

    ats_score = max(
        40,
        min(
            95,
            60 + len(strengths) * 3 - len(weaknesses) * 2
        )
    )

    report = f"ATS Score: {ats_score}/100\n\n"

    report += "Strengths:\n"
    if strengths:
        for s in strengths:
            report += f"• {s}\n"
    else:
        report += "• None\n"

    report += "\nWeaknesses:\n"
    if weaknesses:
        for w in weaknesses:
            report += f"• {w}\n"
    else:
        report += "• None\n"

    report += "\nMissing Skills:\n"
    if missing:
        for m in missing:
            report += f"• {m}\n"
    else:
        report += "• No major missing keywords found.\n"

    report += "\nSuggestions:\n"
    for s in suggestions:
        report += f"• {s}\n"

    return report


# ==========================================================
# ATS ANALYZER
# ==========================================================

def analyze_resume(text):

    if not text.strip():
        return "Resume text is empty."

    if model is None:
        return _local_resume_analysis(text)

    prompt = f"""
You are an experienced ATS recruiter.

Analyze the following resume.

Return ONLY in this format:

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

        if response and hasattr(response, "text"):
            return response.text.strip()

        return _local_resume_analysis(text)

    except Exception as e:
        return (
            _local_resume_analysis(text)
            + f"\n\nGemini note: {e}"
        )


# ==========================================================
# RESUME REWRITER
# ==========================================================

def rewrite_resume(text):

    if not text.strip():
        return "Resume text is empty."

    if model is None:
        return (
            "Gemini API unavailable.\n\n"
            + text
        )

    prompt = f"""
You are a professional resume writer.

Rewrite this resume while:

1. Improving ATS score
2. Fixing grammar
3. Adding a strong professional summary
4. Improving skills section
5. Improving project descriptions
6. Improving experience section

Do NOT invent information.
Keep all original facts.

Resume:

{text}
"""

    try:
        response = model.generate_content(prompt)

        if response and hasattr(response, "text"):
            return response.text.strip()

        return "Resume rewrite failed."

    except Exception as e:
        return f"Rewrite failed: {e}"


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
