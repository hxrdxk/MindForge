from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

from flask_login import current_user

from extensions import db

from models.module import Module
from models.lesson import Lesson

from utils.decorators import teacher_required

from models.lesson import Lesson


teacher_lessons_bp = Blueprint(
    "teacher_lessons",
    __name__,
    url_prefix="/teacher",
)


@teacher_lessons_bp.route(
    "/modules/<int:module_id>/lessons/new",
    methods=["GET", "POST"],
)
@teacher_required
def create_lesson(module_id):

    module = Module.query.get_or_404(module_id)

    if module.course.teacher_id != current_user.id:
        return redirect(url_for("teacher.dashboard"))

    if request.method == "POST":

        title = request.form.get(
            "title",
            ""
        ).strip()

        content = request.form.get(
            "content",
            ""
        ).strip()

        video_url = request.form.get(
            "video_url",
            ""
        ).strip()

        position = int(
            request.form.get(
                "position",
                1,
            )
        )

        if not title:

            flash(
                "Lesson title is required.",
                "danger",
            )

            return redirect(
                url_for(
                    "teacher_lessons.create_lesson",
                    module_id=module.id,
                )
            )

        lesson = Lesson(
            module_id=module.id,
            title=title,
            content=content,
            video_url=video_url,
            position=position,
        )

        db.session.add(lesson)
        db.session.commit()

        flash(
            "Lesson created successfully.",
            "success",
        )

        return redirect(
            url_for(
                "teacher.modules",
                course_id=module.course.id,
            )
        )

    return render_template(
        "teacher/lesson_form.html",
        module=module,
        lesson=None,
    )

@teacher_lessons_bp.route(
    "/lessons/<int:lesson_id>/edit",
    methods=["GET", "POST"],
)
@teacher_required
def edit_lesson(lesson_id):

    lesson = Lesson.query.get_or_404(lesson_id)

    if lesson.module.course.teacher_id != current_user.id:
        return redirect(url_for("teacher.dashboard"))

    if request.method == "POST":

        lesson.title = request.form.get(
            "title",
            ""
        ).strip()

        lesson.video_url = request.form.get(
            "video_url",
            ""
        ).strip()

        lesson.content = request.form.get(
            "content",
            ""
        ).strip()

        lesson.position = int(
            request.form.get(
                "position",
                1,
            )
        )

        db.session.commit()

        flash(
            "Lesson updated successfully.",
            "success",
        )

        return redirect(
            url_for(
                "teacher.modules",
                course_id=lesson.module.course.id,
            )
        )

    return render_template(
        "teacher/lesson_form.html",
        module=lesson.module,
        lesson=lesson,
    )


@teacher_lessons_bp.route(
    "/lessons/<int:lesson_id>/delete"
)
@teacher_required
def delete_lesson(lesson_id):

    lesson = Lesson.query.get_or_404(lesson_id)

    if lesson.module.course.teacher_id != current_user.id:
        return redirect(url_for("teacher.dashboard"))

    course_id = lesson.module.course.id

    db.session.delete(lesson)
    db.session.commit()

    flash(
        "Lesson deleted successfully.",
        "info",
    )

    return redirect(
        url_for(
            "teacher.modules",
            course_id=course_id,
        )
    )