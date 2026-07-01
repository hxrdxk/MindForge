from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

from flask_login import login_required
from flask_login import current_user

from extensions import db

from models.course import Course
from models.enrollment import Enrollment
from models.module import Module
from utils.decorators import teacher_required

teacher_bp = Blueprint(
    "teacher",
    __name__,
    url_prefix="/teacher",
)


@teacher_bp.route("/dashboard")
@teacher_required
def dashboard():

    courses = Course.query.filter_by(
        teacher_id=current_user.id
    ).order_by(
        Course.created_at.desc()
    ).all()

    total_courses = len(courses)

    published_courses = sum(
        1 for c in courses if c.is_published
    )

    total_students = Enrollment.query.join(
        Course
    ).filter(
        Course.teacher_id == current_user.id
    ).count()

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
            teacher_id=current_user.id,
            title=title,
            slug=slug,
            description=description,
            category=category,
            difficulty=difficulty,
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

@teacher_bp.route("/courses/<int:course_id>")
@teacher_required
def manage_course(course_id):

    course = Course.query.filter_by(
        id=course_id,
        teacher_id=current_user.id,
    ).first_or_404()

    return render_template(
        "teacher/manage_course.html",
        course=course,
    )

@teacher_bp.route("/courses/<int:course_id>/modules")
@teacher_required
def modules(course_id):

    course = Course.query.filter_by(
        id=course_id,
        teacher_id=current_user.id,
    ).first_or_404()

    modules = Module.query.filter_by(
        course_id=course.id
    ).order_by(
        Module.position
    ).all()

    return render_template(
        "teacher/modules.html",
        course=course,
        modules=modules,
    )


@teacher_bp.route(
    "/courses/<int:course_id>/modules/new",
    methods=["GET", "POST"],
)
@teacher_required
def create_module(course_id):

    course = Course.query.filter_by(
        id=course_id,
        teacher_id=current_user.id,
    ).first_or_404()

    if request.method == "POST":

        title = request.form.get(
            "title",
            ""
        ).strip()

        description = request.form.get(
            "description",
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
                "Module title is required.",
                "danger",
            )

            return redirect(
                url_for(
                    "teacher.create_module",
                    course_id=course.id,
                )
            )

        module = Module(
            course_id=course.id,
            title=title,
            description=description,
            position=position,
        )

        db.session.add(module)
        db.session.commit()

        flash(
            "Module created successfully.",
            "success",
        )

        return redirect(
            url_for(
                "teacher.modules",
                course_id=course.id,
            )
        )

    return render_template(
        "teacher/module_form.html",
        course=course,
        module=None,
    )


@teacher_bp.route(
    "/modules/<int:module_id>/edit",
    methods=["GET", "POST"],
)
@teacher_required
def edit_module(module_id):

    module = Module.query.get_or_404(module_id)

    if module.course.teacher_id != current_user.id:
        return redirect(url_for("teacher.dashboard"))

    if request.method == "POST":

        module.title = request.form.get(
            "title",
            ""
        ).strip()

        module.description = request.form.get(
            "description",
            ""
        ).strip()

        module.position = int(
            request.form.get(
                "position",
                1,
            )
        )

        db.session.commit()

        flash(
            "Module updated successfully.",
            "success",
        )

        return redirect(
            url_for(
                "teacher.modules",
                course_id=module.course.id,
            )
        )

    return render_template(
        "teacher/module_form.html",
        course=module.course,
        module=module,
    )


@teacher_bp.route("/modules/<int:module_id>/delete")
@teacher_required
def delete_module(module_id):

    module = Module.query.get_or_404(module_id)

    if module.course.teacher_id != current_user.id:
        return redirect(url_for("teacher.dashboard"))

    course_id = module.course.id

    db.session.delete(module)
    db.session.commit()

    flash(
        "Module deleted.",
        "info",
    )

    return redirect(
        url_for(
            "teacher.modules",
            course_id=course_id,
        )
    )