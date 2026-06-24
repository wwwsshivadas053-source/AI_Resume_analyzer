from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        default="user"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    profile_image = db.Column(
        db.String(200),
        default="default.png"
    )

    bio = db.Column(
        db.Text,
        default=""
    )

    linkedin = db.Column(
        db.String(200),
        default=""
    )

    github = db.Column(
        db.String(200),
        default=""
    )

    resumes = db.relationship(
        "ResumeAnalysis",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

class ResumeAnalysis(db.Model):
    __tablename__ = "resume_analysis"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    filename = db.Column(db.String(200))

    ats_score = db.Column(db.Integer)

    match_score = db.Column(
        db.Integer,
        default=0
    )

    job_description = db.Column(db.Text)

    extracted_text = db.Column(db.Text)

    strengths = db.Column(db.Text)

    weaknesses = db.Column(db.Text)

    missing_skills = db.Column(db.Text)

    suggestions = db.Column(db.Text)

    analysis = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

class Feedback(db.Model):
    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    email = db.Column(db.String(100))

    message = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
