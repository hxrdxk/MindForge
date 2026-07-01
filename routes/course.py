from flask import Blueprint
from flask import render_template

from flask_login import (
    login_required,
    current_user,
)

from models.course import Course
from models.enrollment import Enrollment


course_bp = Blueprint(
    "course",
    __name__,
    url_prefix="/courses",
)


@course_bp.route("/")
@login_required
def index():

    courses = Course.query.filter_by(
        is_published=True
    ).order_by(
        Course.created_at.desc()
    ).all()

    return render_template(
        "courses/index.html",
        courses=courses,
    )


@course_bp.route("/<slug>")
@login_required
def details(slug):

    course = Course.query.filter_by(
        slug=slug,
        is_published=True,
    ).first_or_404()

    enrollment = Enrollment.query.filter_by(
        user_id=current_user.id,
        course_id=course.id,
    ).first()

    return render_template(
        "courses/details.html",
        course=course,
        enrollment=enrollment,
    )