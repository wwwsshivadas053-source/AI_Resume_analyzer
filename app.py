import os
from functools import wraps

from flask import Flask, abort, flash, redirect, render_template, request, send_file, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from sqlalchemy import func, inspect, text
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from ats_engine import calculate_ats_score
from config import Config
from gemini_service import analyze_resume, rewrite_resume
from jd_matcher import calculate_match
from models import Feedback, ResumeAnalysis, User, db
from report_generator import generate_report
from resume_parser import extract_resume_text


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message_category = "error"
login_manager.init_app(app)


def admin_required(view):
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if current_user.role != "admin":
            flash("Admin access required.", "error")
            return redirect(url_for("dashboard"))
        return view(*args, **kwargs)

    return wrapped


def ensure_upload_dirs():
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["REPORT_FOLDER"], exist_ok=True)


def ensure_schema():
    """Keep the existing SQLite database usable after model upgrades."""
    inspector = inspect(db.engine)
    table_names = inspector.get_table_names()

    if "users" in table_names:
        columns = {column["name"] for column in inspector.get_columns("users")}
        additions = {
            "role": "VARCHAR(20) DEFAULT 'user'",
            "created_at": "DATETIME",
            "profile_image": "VARCHAR(200) DEFAULT 'default.png'",
            "bio": "TEXT DEFAULT ''",
            "linkedin": "VARCHAR(200) DEFAULT ''",
            "github": "VARCHAR(200) DEFAULT ''",
        }

        for column, definition in additions.items():
            if column not in columns:
                db.session.execute(text(f"ALTER TABLE users ADD COLUMN {column} {definition}"))

    if "resume_analysis" not in table_names:
        db.session.commit()
        return

    columns = {column["name"] for column in inspector.get_columns("resume_analysis")}
    additions = {
        "match_score": "INTEGER DEFAULT 0",
        "job_description": "TEXT",
        "extracted_text": "TEXT",
    }

    for column, definition in additions.items():
        if column not in columns:
            db.session.execute(text(f"ALTER TABLE resume_analysis ADD COLUMN {column} {definition}"))
    db.session.commit()


def seed_admin():
    email = os.getenv("ADMIN_EMAIL", "admin@resumeai.local")
    password = os.getenv("ADMIN_PASSWORD", "Admin@123")
    username = os.getenv("ADMIN_USERNAME", "Project Admin")

    admin = User.query.filter_by(email=email).first()
    if admin:
        if admin.role != "admin":
            admin.role = "admin"
            db.session.commit()
        return

    db.session.add(
        User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            role="admin",
        )
    )
    db.session.commit()


with app.app_context():
    ensure_upload_dirs()
    db.create_all()
    ensure_schema()
    seed_admin()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.context_processor
def inject_stats():
    return {"site_name": "ResumeAI Pro"}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("admin_dashboard" if current_user.role == "admin" else "dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not username or not email or len(password) < 6:
            flash("Enter a name, valid email, and password with at least 6 characters.", "error")
            return redirect(url_for("register"))

        if User.query.filter_by(email=email).first():
            flash("An account with this email already exists.", "error")
            return redirect(url_for("register"))

        user = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            role="user",
        )
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin_dashboard" if current_user.role == "admin" else "dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Welcome back.", "success")
            return redirect(url_for("admin_dashboard" if user.role == "admin" else "dashboard"))

        flash("Invalid email or password.", "error")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for("home"))


@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.role == "admin":
        return redirect(url_for("admin_dashboard"))

    analyses = (
        ResumeAnalysis.query.filter_by(user_id=current_user.id)
        .order_by(ResumeAnalysis.created_at.desc())
        .all()
    )
    return render_template("dashboard.html", analyses=analyses)


@app.route("/analyzer", methods=["GET", "POST"])
@login_required
def analyzer():
    result = None
    score = None
    match_score = None
    filename = None

    if request.method == "POST":
        file = request.files.get("resume")
        jd = request.form.get("job_description", "").strip()

        if not file or not file.filename:
            flash("Upload a PDF resume.", "error")
            return redirect(url_for("analyzer"))

        filename = secure_filename(file.filename)
        if not filename.lower().endswith(".pdf"):
            flash("Only PDF resumes are supported.", "error")
            return redirect(url_for("analyzer"))

        path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(path)

        try:
            text_content = extract_resume_text(path)
        except Exception as exc:
            flash(f"Could not read the PDF: {exc}", "error")
            return redirect(url_for("analyzer"))

        if not text_content.strip():
            flash("No readable text was found in the PDF.", "error")
            return redirect(url_for("analyzer"))

        score = calculate_ats_score(text_content)
        match_score = calculate_match(text_content, jd) if jd else 0
        result = analyze_resume(text_content)

        analysis = ResumeAnalysis(
            user_id=current_user.id,
            filename=filename,
            ats_score=score,
            match_score=match_score,
            job_description=jd,
            extracted_text=text_content[:15000],
            analysis=result,
        )
        db.session.add(analysis)
        db.session.commit()
        flash("Resume analyzed and saved to your dashboard.", "success")

    return render_template(
        "analyzer.html",
        result=result,
        score=score,
        match_score=match_score,
        filename=filename,
    )


@app.route("/feedback", methods=["POST"])
def feedback():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    message = request.form.get("message", "").strip()

    if not name or not email or not message:
        flash("Please complete all feedback fields.", "error")
        return redirect(url_for("home"))

    db.session.add(Feedback(name=name, email=email, message=message))
    db.session.commit()
    flash("Feedback submitted. Thank you.", "success")
    return redirect(url_for("home"))


@app.route("/download-report/<int:id>")
@login_required
def download_report(id):
    analysis = ResumeAnalysis.query.get_or_404(id)
    if current_user.role != "admin" and analysis.user_id != current_user.id:
        abort(403)

    pdf = generate_report(analysis.filename, analysis.ats_score, analysis.analysis)
    return send_file(pdf, as_attachment=True)


@app.route("/rewrite/<int:id>")
@login_required
def rewrite(id):
    analysis = ResumeAnalysis.query.get_or_404(id)
    if current_user.role != "admin" and analysis.user_id != current_user.id:
        abort(403)

    rewritten = rewrite_resume(analysis.extracted_text or analysis.analysis or "")
    return render_template("rewrite.html", rewritten=rewritten)


@app.route("/admin")
@admin_required
def admin_dashboard():
    users = User.query.count()
    feedbacks = Feedback.query.count()
    resumes = ResumeAnalysis.query.count()
    average_score = db.session.query(func.avg(ResumeAnalysis.ats_score)).scalar() or 0
    recent_logs = ResumeAnalysis.query.order_by(ResumeAnalysis.created_at.desc()).limit(5).all()

    return render_template(
        "admin/dashboard.html",
        users=users,
        feedbacks=feedbacks,
        resumes=resumes,
        average_score=round(average_score, 1),
        recent_logs=recent_logs,
    )


@app.route("/admin/users", methods=["GET", "POST"])
@admin_required
def admin_users():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        role = request.form.get("role", "user")

        if role not in {"user", "admin"}:
            role = "user"

        if not username or not email or len(password) < 6:
            flash("User creation requires name, email, and a 6+ character password.", "error")
            return redirect(url_for("admin_users"))

        if User.query.filter_by(email=email).first():
            flash("A user with that email already exists.", "error")
            return redirect(url_for("admin_users"))

        db.session.add(
            User(
                username=username,
                email=email,
                password=generate_password_hash(password),
                role=role,
            )
        )
        db.session.commit()
        flash("User created.", "success")
        return redirect(url_for("admin_users"))

    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/users.html", users=users)


@app.route("/admin/users/<int:id>/role", methods=["POST"])
@admin_required
def update_user_role(id):
    user = User.query.get_or_404(id)
    role = request.form.get("role", "user")
    if role not in {"user", "admin"}:
        flash("Invalid role.", "error")
        return redirect(url_for("admin_users"))

    user.role = role
    db.session.commit()
    flash("User role updated.", "success")
    return redirect(url_for("admin_users"))


@app.route("/admin/users/<int:id>/delete", methods=["POST"])
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        flash("You cannot delete the account you are using.", "error")
        return redirect(url_for("admin_users"))

    db.session.delete(user)
    db.session.commit()
    flash("User deleted.", "success")
    return redirect(url_for("admin_users"))


@app.route("/admin/feedback")
@admin_required
def admin_feedback():
    feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).all()
    return render_template("admin/feedback.html", feedbacks=feedbacks)


@app.route("/admin/feedback/<int:id>/delete", methods=["POST"])
@admin_required
def delete_feedback(id):
    item = Feedback.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash("Feedback deleted.", "success")
    return redirect(url_for("admin_feedback"))


@app.route("/admin/logs")
@admin_required
def admin_logs():
    logs = ResumeAnalysis.query.order_by(ResumeAnalysis.created_at.desc()).all()
    return render_template("admin/logs.html", logs=logs)


@app.route("/admin/logs/<int:id>/delete", methods=["POST"])
@admin_required
def delete_log(id):
    log = ResumeAnalysis.query.get_or_404(id)
    db.session.delete(log)
    db.session.commit()
    flash("Analyzer log deleted.", "success")
    return redirect(url_for("admin_logs"))


if __name__ == "__main__":
    app.run(debug=True)
