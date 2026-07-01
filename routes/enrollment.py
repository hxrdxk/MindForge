from flask import (
    Blueprint,
    redirect,
    url_for,
    flash,
)

from flask_login import (
    login_required,
    current_user,
)

from extensions import db
from models.course import Course
from models.enrollment import Enrollment


enrollment_bp = Blueprint(
    "enrollment",
    __name__,
    url_prefix="/enrollment",
)


@enrollment_bp.route("/<int:course_id>")
@login_required
def enroll(course_id):

    course = Course.query.get_or_404(course_id)

    existing = Enrollment.query.filter_by(
        user_id=current_user.id,
        course_id=course.id,
    ).first()

    if existing:

        flash(
            "You are already enrolled in this course.",
            "warning",
        )

        return redirect(
            url_for("course.index")
        )

    enrollment = Enrollment(
        user_id=current_user.id,
        course_id=course.id,
    )

    db.session.add(enrollment)
    db.session.commit()

    flash(
        "Course enrolled successfully.",
        "success",
    )

    return redirect(
        url_for("student.dashboard")
    )