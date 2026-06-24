import re

def calculate_match(resume_text, job_description):

    resume_text = resume_text.lower()

    jd = job_description.lower()

    words = set(re.findall(r'\w+', jd))

    matched = 0

    for word in words:

        if word in resume_text:
            matched += 1

    if len(words) == 0:
        return 0

    return int((matched / len(words)) * 100)