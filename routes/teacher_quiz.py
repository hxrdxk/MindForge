from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)
from flask_login import current_user
from models.module import Module
from extensions import db
from flask_login import login_required
from utils.decorators import teacher_required
from models.quiz import Quiz
from models.question import Question
from models.option import Option

teacher_quiz_bp = Blueprint(
    "teacher_quiz",
    __name__,
    url_prefix="/teacher",
)

@teacher_quiz_bp.route(
    "/modules/<int:module_id>/quiz",
    methods=["GET", "POST"],
)
@teacher_required
def create_quiz(module_id):

    module = Module.query.get_or_404(module_id)

    if module.course.teacher_id != current_user.id:
        return redirect(url_for("teacher.dashboard"))

    quiz = module.quiz

    if quiz:
        return redirect(
            url_for(
                "teacher_quiz.manage_quiz",
                quiz_id=quiz.id,
            )
        )

    if request.method == "POST":

        quiz = Quiz(
            module_id=module.id,
            title=request.form["title"],
            description=request.form["description"],
            passing_score=int(
                request.form["passing_score"]
            ),
            is_published=False,
        )

        db.session.add(quiz)
        db.session.commit()

        flash(
            "Quiz created successfully.",
            "success",
        )

        return redirect(
            url_for(
                "teacher_quiz.manage_quiz",
                quiz_id=quiz.id,
            )
        )

    return render_template(
        "teacher/quiz_form.html",
        module=module,
    )

@teacher_quiz_bp.route("/quiz/<int:quiz_id>")
@teacher_required
def manage_quiz(quiz_id):

    quiz = Quiz.query.get_or_404(quiz_id)

    if quiz.module.course.teacher_id != current_user.id:
        return redirect(url_for("teacher.dashboard"))

    return render_template(
        "teacher/question_form.html",
        quiz=quiz,
    )

@teacher_quiz_bp.route(
    "/quiz/<int:quiz_id>/question/add",
    methods=["GET", "POST"],
)
@teacher_required
def add_question(quiz_id):

    quiz = Quiz.query.get_or_404(quiz_id)

    if quiz.module.course.teacher_id != current_user.id:
        return redirect(url_for("teacher.dashboard"))

    if request.method == "POST":

        question = Question(
            quiz_id=quiz.id,
            question_text=request.form.get(
                "question_text",
                "",
            ).strip(),
            question_type=request.form.get(
                "question_type",
                "mcq",
            ),
            points=int(
                request.form.get(
                    "points",
                    1,
                )
            ),
            position=int(
                request.form.get(
                    "position",
                    1,
                )
            ),
        )

        db.session.add(question)
        db.session.flush()

        if question.question_type == "mcq":

            for i in range(4):

                option = Option(
                    question_id=question.id,
                    option_text=f"Option {chr(65 + i)}",
                    is_correct=False,
                )

                db.session.add(option)

        else:

            db.session.add(
                Option(
                    question_id=question.id,
                    option_text="True",
                    is_correct=False,
                )
            )

            db.session.add(
                Option(
                    question_id=question.id,
                    option_text="False",
                    is_correct=False,
                )
            )

        db.session.commit()
        flash(
            "Question created successfully.",
            "success",
        )

        return redirect(
            url_for(
                "teacher_quiz.manage_quiz",
                quiz_id=quiz.id,
            )
        )

    return render_template(
        "teacher/add_question.html",
        quiz=quiz,
    )

@teacher_quiz_bp.route(
    "/question/<int:question_id>/edit",
    methods=["GET", "POST"],
)
@teacher_required
def edit_question(question_id):

    question = Question.query.get_or_404(question_id)

    if question.quiz.module.course.teacher_id != current_user.id:
        return redirect(url_for("teacher.dashboard"))

    if request.method == "POST":

        question.question_text = request.form.get(
            "question_text",
            "",
        ).strip()

        question.points = int(
            request.form.get("points", 1)
        )

        for option in question.options:

            option.option_text = request.form.get(
                f"option_{option.id}",
                option.option_text,
            )

            option.is_correct = (
                request.form.get("correct_option")
                == str(option.id)
            )

        db.session.commit()

        flash(
            "Question updated successfully.",
            "success",
        )

        return redirect(
            url_for(
                "teacher_quiz.manage_quiz",
                quiz_id=question.quiz.id,
            )
        )

    return render_template(
        "teacher/edit_question.html",
        question=question,
    )

@teacher_quiz_bp.route(
    "/quiz/<int:quiz_id>/publish",
    methods=["POST"],
)
@teacher_required
def publish_quiz(quiz_id):

    quiz = Quiz.query.get_or_404(quiz_id)

    if quiz.module.course.teacher_id != current_user.id:
        return redirect(url_for("teacher.dashboard"))
    
    if not quiz.is_published:

        if not quiz.questions:

            flash(
                "Add at least one question before publishing.",
                "danger",
            )

            return redirect(
                url_for(
                    "teacher_quiz.manage_quiz",
                    quiz_id=quiz.id,
                )
            )

        for question in quiz.questions:

            correct_answers = sum(
                1
                for option in question.options
                if option.is_correct
            )

            if correct_answers != 1:

                flash(
                    f'Question "{question.question_text}" '
                    "must have exactly one correct answer.",
                    "danger",
                )

                return redirect(
                    url_for(
                        "teacher_quiz.manage_quiz",
                        quiz_id=quiz.id,
                    )
                )

    quiz.is_published = not quiz.is_published

    db.session.commit()

    if quiz.is_published:

        flash(
            "Quiz published successfully.",
            "success",
        )

    else:

        flash(
            "Quiz unpublished.",
            "info",
        )

    return redirect(
        url_for(
            "teacher_quiz.manage_quiz",
            quiz_id=quiz.id,
        )
    )