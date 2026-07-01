from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

from flask_login import login_required

from extensions import db

from models.course import Course
from models.enrollment import Enrollment
from utils.decorators import teacher_required

teacher_bp = Blueprint(
    "teacher",
    __name__,
    url_prefix="/teacher",
)


@teacher_bp.route("/dashboard")
@teacher_required
def dashboard():

    courses = Course.query.order_by(
        Course.created_at.desc()
    ).all()

    total_courses = len(courses)

    published_courses = sum(
        1 for c in courses if c.is_published
    )

    total_students = Enrollment.query.count()

    if total_students:

        average_progress = round(
            sum(
                e.progress
                for e in Enrollment.query.all()
            ) / total_students,
            1,
        )

    else:

        average_progress = 0

    return render_template(
        "teacher/dashboard.html",
        courses=courses,
        total_courses=total_courses,
        published_courses=published_courses,
        total_students=total_students,
        average_progress=average_progress,
    )


@teacher_bp.route(
    "/courses/create",
    methods=["GET", "POST"],
)
@teacher_required
def create_course():

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        slug = request.form.get("slug", "").strip().lower()
        category = request.form.get("category", "").strip()
        difficulty = request.form.get("difficulty")
        description = request.form.get("description").strip()

        if not title or not slug:

            flash(
                "Title and Slug are required.",
                "danger",
            )

            return redirect(
                url_for("teacher.create_course")
            )

        if Course.query.filter_by(slug=slug).first():

            flash(
                "Slug already exists.",
                "warning",
            )

            return redirect(
                url_for("teacher.create_course")
            )

        course = Course(
            title=title,
            slug=slug,
            category=category,
            difficulty=difficulty,
            description=description,
            is_published=True,
        )

        db.session.add(course)
        db.session.commit()

        flash(
            "Course created successfully.",
            "success",
        )

        return redirect(
            url_for("teacher.dashboard")
        )

    return render_template(
        "teacher/create_course.html"
    )