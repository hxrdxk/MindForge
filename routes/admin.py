from flask import Blueprint
from flask import render_template

from flask_login import login_required

from utils.decorators import admin_required

from models.user import User
from models.course import Course
from models.enrollment import Enrollment
from models.certificate import Certificate
from models.quiz_attempt import QuizAttempt


admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin",
)


@admin_bp.route("/dashboard")
@login_required
@admin_required
def dashboard():

    total_users = User.query.count()

    total_students = User.query.filter_by(
        role="student"
    ).count()

    total_teachers = User.query.filter_by(
        role="teacher"
    ).count()

    total_courses = Course.query.count()

    total_enrollments = Enrollment.query.count()

    total_certificates = Certificate.query.count()

    total_quiz_attempts = QuizAttempt.query.count()

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_students=total_students,
        total_teachers=total_teachers,
        total_courses=total_courses,
        total_enrollments=total_enrollments,
        total_certificates=total_certificates,
        total_quiz_attempts=total_quiz_attempts,
    )

@admin_bp.route("/users")
@login_required
@admin_required
def users():

    users = User.query.order_by(
        User.created_at.desc()
    ).all()

    return render_template(
        "admin/users.html",
        users=users,
    )

@admin_bp.route("/courses")
@login_required
@admin_required
def courses():

    courses = Course.query.order_by(
        Course.created_at.desc()
    ).all()

    course_stats = []

    for course in courses:

        total_students = Enrollment.query.filter_by(
            course_id=course.id
        ).count()

        course_stats.append({
            "course": course,
            "students": total_students,
        })

    return render_template(
        "admin/courses.html",
        course_stats=course_stats,
    )

@admin_bp.route("/certificates")
@login_required
@admin_required
def certificates():

    certificates = Certificate.query.order_by(
        Certificate.issued_at.desc()
    ).all()

    return render_template(
        "admin/certificates.html",
        certificates=certificates,
    )