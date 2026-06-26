# 🚀 AI Resume Analyzer

> An AI-powered Resume Analyzer built with **Flask**, **Google Gemini AI**, and **PDF Processing** that evaluates resumes, calculates ATS compatibility, matches resumes with job descriptions, rewrites resumes using AI, and generates downloadable reports.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black)
![Gemini](https://img.shields.io/badge/Google-Gemini-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

---

# 📖 Overview

AI Resume Analyzer is a modern web application that helps students and job seekers improve their resumes using Artificial Intelligence.

The system extracts text from uploaded PDF resumes, analyzes ATS compatibility, identifies missing skills, compares resumes against job descriptions, rewrites resumes professionally using Google's Gemini AI, and generates detailed downloadable reports.

This project demonstrates practical implementation of:

- Artificial Intelligence
- Large Language Models (LLMs)
- Natural Language Processing
- PDF Processing
- Flask Web Development
- Authentication
- CRUD Operations
- Report Generation

---

# ✨ Features

## 👤 User Features

- User Registration & Login
- Secure Authentication
- Upload Resume (PDF)
- Resume Text Extraction
- ATS Score Analysis
- AI Resume Review
- Resume Rewriter
- Job Description Matching
- Missing Skills Detection
- Professional Suggestions
- Download PDF Report
- Submit Feedback

---

## 🤖 AI Features

- Gemini AI Integration
- ATS Score Prediction
- Resume Improvement Suggestions
- Resume Rewriting
- Keyword Analysis
- Grammar Improvement
- Skills Recommendation
- Professional Summary Generation

---

## 🛠 Admin Features

- Admin Dashboard
- User Management
- Resume Management
- Feedback Management
- Analytics Dashboard

---

# 📸 Screenshots

Add screenshots here after deployment.

<img width="1351" height="637" alt="Screenshot 2026-06-26 102419" src="https://github.com/user-attachments/assets/5c169c30-8b49-41d7-b22c-904b3428bb12" />

<img width="1347" height="636" alt="Screenshot 2026-06-26 101938" src="https://github.com/user-attachments/assets/e3545879-e914-4237-8ce8-f758b8bcce3b" />

<img width="1352" height="639" alt="Screenshot 2026-06-26 102034" src="https://github.com/user-attachments/assets/4ecdab7a-d727-49ec-8a42-332b61aa9a3e" />

<img width="1349" height="639" alt="Screenshot 2026-06-26 102151" src="https://github.com/user-attachments/assets/9fdc9a4d-d004-4318-bb0e-b3baf781906a" />

<img width="1352" height="638" alt="Screenshot 2026-06-26 104016" src="https://github.com/user-attachments/assets/d1c22eec-f21e-44f0-aa9a-38400a748d83" />

<img width="1351" height="636" alt="Screenshot 2026-06-26 104059" src="https://github.com/user-attachments/assets/9fbb017a-6183-485f-a906-b352334f3fb1" />

<img width="1364" height="637" alt="Screenshot 2026-06-26 102315" src="https://github.com/user-attachments/assets/dd7387a9-8813-414f-a161-79b090441359" />

<img width="1351" height="639" alt="Screenshot 2026-06-26 104203" src="https://github.com/user-attachments/assets/48fa12a4-1365-49b2-b102-86336a72e453" />


---

# 🏗 Project Structure

```
Resume-Analyzer/
│
├── app.py
├── ats_engine.py
├── gemini_service.py
├── resume_parser.py
├── jd_matcher.py
├── report_generator.py
├── models.py
├── config.py
├── requirements.txt
│
├── templates/
│
├── static/
│   ├── css/
│   ├── js/
│   ├── uploads/
│   └── reports/
│
├── admin/
│
├── migrations/
│
└── instance/
```

---

# ⚙ Tech Stack

### Frontend

- HTML5
- CSS3
- Tailwind CSS
- JavaScript

### Backend

- Python
- Flask

### Database

- SQLite
- SQLAlchemy

### AI

- Google Gemini API

### Libraries

- PyPDF2
- pdfplumber
- Flask-Login
- Flask-WTF
- Flask-Migrate
- ReportLab

---

# 📦 Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/resume-analyzer.git

cd resume-analyzer
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the project root.

```env
SECRET_KEY=your_secret_key

GEMINI_API_KEY=your_gemini_api_key
```

Example:

```env
SECRET_KEY=abc123xyz

GEMINI_API_KEY=AIzaSyXXXXXXXXXXXX
```

---

# ▶ Run Application

```bash
python app.py
```

Application will start at

```
http://127.0.0.1:5000
```

---

# ☁ Deploy on Render

1. Push project to GitHub.

2. Create a new Web Service on Render.

3. Connect GitHub repository.

4. Build Command

```bash
pip install -r requirements.txt
```

5. Start Command

```bash
gunicorn app:app
```

6. Add Environment Variables

```
SECRET_KEY

GEMINI_API_KEY
```

Deploy 🎉

---

# 📊 ATS Analysis

The analyzer provides:

- ATS Score
- Resume Strengths
- Weaknesses
- Missing Skills
- Keyword Matching
- AI Suggestions
- Resume Rewrite
- Job Description Match Score

---

# 🤖 AI Workflow

```
Upload Resume
        │
        ▼
Extract PDF Text
        │
        ▼
Gemini AI Analysis
        │
        ▼
ATS Score
        │
        ▼
Suggestions
        │
        ▼
Resume Rewrite
        │
        ▼
Generate PDF Report
```

---

# 📄 Sample Output

```
ATS Score: 87/100

Strengths
✔ Strong Python Skills
✔ Flask Experience
✔ Multiple AI Projects

Weaknesses
• Missing Quantified Achievements
• Weak Professional Summary

Suggestions
• Add measurable impact
• Improve project descriptions
• Include certifications
```

---

# 🎯 Future Improvements

- Multiple Resume Templates
- Resume Ranking
- Cover Letter Generator
- LinkedIn Profile Analysis
- AI Interview Questions
- Skill Gap Analysis
- Multi-language Support
- Email Resume Reports
- Resume Version History
- Recruiter Dashboard

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository

2. Create a feature branch

```bash
git checkout -b feature-name
```

3. Commit changes

```bash
git commit -m "Added new feature"
```

4. Push branch

```bash
git push origin feature-name
```

5. Open a Pull Request

---

# 📜 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Prajwal T S**

Python Developer | AI & ML Enthusiast

GitHub: https://github.com/wwwsshivadas053-source

---

# ⭐ Support

If you found this project useful,

⭐ Star the repository

🍴 Fork the project

📢 Share it with others

---

## 💼 Resume Project Highlights

- AI-powered Resume Analysis
- ATS Score Prediction
- Google Gemini Integration
- Resume Rewriting
- Job Description Matching
- PDF Report Generation
- User Authentication
- Admin Dashboard
- Responsive UI
- Production Ready Flask Application
