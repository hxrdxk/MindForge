from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from flask_login import current_user
from flask import send_file
from utils.decorators import student_required
from models.enrollment import Enrollment
from models.course import Course
from models.lesson import Lesson
from datetime import datetime
from models.lesson_progress import LessonProgress
from extensions import db
from models.quiz import Quiz
from models.quiz_attempt import QuizAttempt
from models.answer import Answer
from models.option import Option
from models.question import Question
from models.certificate import Certificate
from utils.pdf import generate_certificate_pdf

student_bp = Blueprint(
    "student",
    __name__,
    url_prefix="/student",
)

def update_course_progress(enrollment):

    total_lessons = sum(
        len(module.lessons)
        for module in enrollment.course.modules
    )

    completed_lessons = LessonProgress.query.filter_by(
        enrollment_id=enrollment.id,
        completed=True,
    ).count()

    if total_lessons:

        enrollment.progress = round(
            completed_lessons / total_lessons * 100,
            1,
        )

    else:

        enrollment.progress = 0

    course_completed = True

    for module in enrollment.course.modules:

        if module.lessons:

            module_completed_lessons = sum(

                1

                for lesson in module.lessons

                if LessonProgress.query.filter_by(
                    enrollment_id=enrollment.id,
                    lesson_id=lesson.id,
                    completed=True,
                ).first()

            )

            if module_completed_lessons != len(module.lessons):

                course_completed = False
                break

        if (
            module.quiz
            and module.quiz.is_published
        ):

            passed_attempt = QuizAttempt.query.filter_by(
                enrollment_id=enrollment.id,
                quiz_id=module.quiz.id,
                passed=True,
            ).first()

            if not passed_attempt:

                course_completed = False
                break

    enrollment.completed = course_completed

    db.session.commit()

def issue_certificate(enrollment):

    if not enrollment.completed:
        return

    from models.certificate import Certificate

    existing = Certificate.query.filter_by(
        enrollment_id=enrollment.id,
    ).first()

    if existing:
        return

    attempts = []

    for module in enrollment.course.modules:

        if module.quiz:

            best_attempt = (
                QuizAttempt.query.filter_by(
                    enrollment_id=enrollment.id,
                    quiz_id=module.quiz.id,
                    passed=True,
                )
                .order_by(
                    QuizAttempt.score.desc()
                )
                .first()
            )

            if best_attempt:

                attempts.append(best_attempt.score)

    final_score = (
        round(
            sum(attempts) / len(attempts),
            1,
        )
        if attempts
        else 100
    )

    certificate = Certificate(

        certificate_id=(
            f"MF-"
            f"{datetime.utcnow().year}-"
            f"{enrollment.id:06d}"
        ),

        enrollment_id=enrollment.id,

        final_score=final_score,

    )

    db.session.add(certificate)

    db.session.commit()

def get_completed_lessons(enrollment):

    return {
        progress.lesson_id
        for progress in enrollment.lesson_progress
        if progress.completed
    }

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

    certificate_count = sum(
        1
        for enrollment in enrollments
        if enrollment.certificate
    )

    return render_template(
        "student/dashboard.html",
        enrollments=enrollments,
        total_courses=total_courses,
        completed_courses=completed_courses,
        certificate_count=certificate_count,
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

    completed_lessons = get_completed_lessons(
        enrollment
    )

    quiz_status = {}

    for module in course.modules:

        if not module.quiz:

            continue

        attempts = (
            QuizAttempt.query.filter_by(
                enrollment_id=enrollment.id,
                quiz_id=module.quiz.id,
            )
            .order_by(
                QuizAttempt.submitted_at.desc()
            )
            .all()
        )

        if not attempts:

            quiz_status[module.id] = {

                "attempted": False,
                "passed": False,
                "best_score": 0,
                "latest_score": 0,
                "attempts": 0,

            }

            continue

        best_score = max(
            attempt.score
            for attempt in attempts
        )

        latest_attempt = attempts[0]

        quiz_status[module.id] = {

            "attempted": True,
            "passed": any(
                attempt.passed
                for attempt in attempts
            ),
            "best_score": best_score,
            "latest_score": latest_attempt.score,
            "attempts": len(attempts),

        }

    return render_template(
        "student/course_curriculum.html",
        course=course,
        enrollment=enrollment,
        completed_lessons=completed_lessons,
        quiz_status=quiz_status,
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

    completed = LessonProgress.query.filter_by(
        enrollment_id=enrollment.id,
        lesson_id=lesson.id,
        completed=True,
    ).first()
    
    return render_template(
        "student/lesson_view.html",
        lesson=lesson,
        enrollment=enrollment,
        previous_lesson=previous_lesson,
        next_lesson=next_lesson,
        completed=completed,
    )

@student_bp.route(
    "/lessons/<int:lesson_id>/complete",
    methods=["POST"],
)
@student_required
def complete_lesson(lesson_id):

    lesson = Lesson.query.get_or_404(lesson_id)

    enrollment = Enrollment.query.filter_by(
        user_id=current_user.id,
        course_id=lesson.module.course.id,
    ).first_or_404()

    progress = LessonProgress.query.filter_by(
        enrollment_id=enrollment.id,
        lesson_id=lesson.id,
    ).first()

    if progress is None:

        progress = LessonProgress(
            enrollment_id=enrollment.id,
            lesson_id=lesson.id,
        )

        db.session.add(progress)

    progress.mark_complete()

    update_course_progress(enrollment)

    db.session.commit()

    flash(
        "Lesson marked as completed.",
        "success",
    )

    next_lesson = None

    modules = lesson.module.course.modules

    all_lessons = []

    for module in sorted(modules, key=lambda m: m.position):
        all_lessons.extend(
            sorted(
                module.lessons,
                key=lambda l: l.position,
            )
        )

    current_index = all_lessons.index(lesson)

    if current_index < len(all_lessons) - 1:
        next_lesson = all_lessons[current_index + 1]

    db.session.commit()

    if next_lesson:

        return redirect(
            url_for(
                "student.lesson_view",
                lesson_id=next_lesson.id,
            )
        )

    flash(
        "🎉 Congratulations! You have completed this course.",
        "success",
    )

    return redirect(
        url_for(
            "student.course_curriculum",
            course_id=lesson.module.course.id,
        )
    )

@student_bp.route(
    "/quiz/<int:quiz_id>",
    methods=["GET", "POST"],
)
@student_required
def take_quiz(quiz_id):

    quiz = Quiz.query.get_or_404(quiz_id)

    if not quiz.is_published:

        flash(
            "This quiz is not available.",
            "warning",
        )

        return redirect(
            url_for(
                "student.course_curriculum",
                course_id=quiz.module.course.id,
            )
        )

    enrollment = Enrollment.query.filter_by(
        user_id=current_user.id,
        course_id=quiz.module.course.id,
    ).first_or_404()

    if request.method == "POST":

        attempt = QuizAttempt(
            enrollment_id=enrollment.id,
            quiz_id=quiz.id,
        )

        db.session.add(attempt)
        db.session.flush()

        total_points = 0
        earned_points = 0

        for question in quiz.questions:

            selected = request.form.get(
                f"question_{question.id}"
            )

            if not selected:
                continue

            selected_option = Option.query.get(
                int(selected)
            )

            correct = selected_option.is_correct

            if correct:
                earned_points += question.points

            total_points += question.points

            db.session.add(
                Answer(
                    attempt_id=attempt.id,
                    question_id=question.id,
                    selected_option_id=selected_option.id,
                    is_correct=correct,
                )
            )

        if total_points:

            score = round(
                earned_points / total_points * 100,
                1,
            )

        else:

            score = 0

        attempt.score = score

        attempt.passed = (
            score >= quiz.passing_score
        )

        db.session.commit()

        update_course_progress(enrollment)

        issue_certificate(enrollment)

        return redirect(
            url_for(
                "student.quiz_result",
                attempt_id=attempt.id,
            )
        )
    
    return render_template(
        "student/quiz.html",
        quiz=quiz,
    )

@student_bp.route(
    "/quiz/result/<int:attempt_id>"
)
@student_required
def quiz_result(attempt_id):

    attempt = QuizAttempt.query.get_or_404(
        attempt_id
    )

    if attempt.enrollment.user_id != current_user.id:

        flash(
            "Unauthorized access.",
            "danger",
        )

        return redirect(
            url_for(
                "student.dashboard"
            )
        )

    review = []

    correct_count = 0

    for answer in attempt.answers:

        question = answer.question

        correct_option = next(
            (
                option
                for option in question.options
                if option.is_correct
            ),
            None,
        )

        review.append({

            "question": question,

            "selected_option": answer.selected_option,

            "correct_option": correct_option,

            "is_correct": answer.is_correct,

        })

        if answer.is_correct:

            correct_count += 1

    total_questions = len(review)

    incorrect_count = (
        total_questions - correct_count
    )

    return render_template(
        "student/quiz_result.html",
        attempt=attempt,
        review=review,
        correct_count=correct_count,
        incorrect_count=incorrect_count,
        total_questions=total_questions,
    )

@student_bp.route("/certificates")
@student_required
def certificates():

    certificates = (
        Certificate.query.join(Enrollment)
        .filter(
            Enrollment.user_id == current_user.id
        )
        .order_by(
            Certificate.issued_at.desc()
        )
        .all()
    )

    return render_template(
        "student/certificates.html",
        certificates=certificates,
    )


@student_bp.route(
    "/certificate/<int:certificate_id>"
)
@student_required
def view_certificate(certificate_id):

    certificate = (
        Certificate.query.get_or_404(
            certificate_id
        )
    )

    if (
        certificate.enrollment.user_id
        != current_user.id
    ):

        flash(
            "Unauthorized access.",
            "danger",
        )

        return redirect(
            url_for(
                "student.dashboard"
            )
        )

    return render_template(
        "student/certificate.html",
        certificate=certificate,
    )

@student_bp.route(
    "/certificate/<int:certificate_id>/download"
)
@student_required
def download_certificate(certificate_id):

    certificate = Certificate.query.get_or_404(
        certificate_id
    )

    if (
        certificate.enrollment.user_id
        != current_user.id
    ):

        flash(
            "Unauthorized access.",
            "danger",
        )

        return redirect(
            url_for(
                "student.dashboard"
            )
        )

    pdf = generate_certificate_pdf(
        certificate
    )

    filename = (
        f"{certificate.certificate_id}.pdf"
    )

    return send_file(
        pdf,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=filename,
    )

