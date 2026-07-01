from flask import Blueprint
from flask import render_template
from flask_login import login_required
from flask_login import current_user
from utils.decorators import student_required
from models.enrollment import Enrollment
from models.course import Course
from models.lesson import Lesson

student_bp = Blueprint(
    "student",
    __name__,
    url_prefix="/student",
)


@student_bp.route("/dashboard")
@student_required
def dashboard():

    enrollments = Enrollment.query.filter_by(
        user_id=current_user.id
    ).all()

    total_courses = len(enrollments)

    completed_courses = sum(
        1 for e in enrollments if e.completed
    )

    if total_courses:

        overall_progress = (
            sum(e.progress for e in enrollments)
            / total_courses
        )

    else:

        overall_progress = 0

    return render_template(
        "student/dashboard.html",
        enrollments=enrollments,
        total_courses=total_courses,
        completed_courses=completed_courses,
        overall_progress=round(
            overall_progress,
            1,
        ),
    )

@student_bp.route("/courses")
@student_required
def my_courses():

    enrollments = Enrollment.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Enrollment.enrolled_at.desc()
    ).all()

    return render_template(
        "student/my_courses.html",
        enrollments=enrollments,
    )

@student_bp.route("/courses/<int:course_id>")
@student_required
def course_curriculum(course_id):

    enrollment = Enrollment.query.filter_by(
        user_id=current_user.id,
        course_id=course_id,
    ).first_or_404()

    course = Course.query.get_or_404(course_id)

    return render_template(
        "student/course_curriculum.html",
        course=course,
        enrollment=enrollment,
    )

@student_bp.route("/lessons/<int:lesson_id>")
@student_required
def lesson_view(lesson_id):

    lesson = Lesson.query.get_or_404(lesson_id)

    enrollment = Enrollment.query.filter_by(
        user_id=current_user.id,
        course_id=lesson.module.course.id,
    ).first_or_404()

    modules = lesson.module.course.modules

    lessons = []

    for module in modules:
        lessons.extend(module.lessons)

    lessons = sorted(
        lessons,
        key=lambda l: (
            l.module.position,
            l.position,
        ),
    )

    current_index = lessons.index(lesson)

    previous_lesson = (
        lessons[current_index - 1]
        if current_index > 0
        else None
    )

    next_lesson = (
        lessons[current_index + 1]
        if current_index < len(lessons) - 1
        else None
    )

    return render_template(
        "student/lesson_view.html",
        lesson=lesson,
        enrollment=enrollment,
        previous_lesson=previous_lesson,
        next_lesson=next_lesson,
    )