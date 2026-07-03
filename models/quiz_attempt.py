from datetime import datetime

from extensions import db


class QuizAttempt(db.Model):

    __tablename__ = "quiz_attempts"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    enrollment_id = db.Column(
        db.Integer,
        db.ForeignKey("enrollments.id"),
        nullable=False,
    )

    quiz_id = db.Column(
        db.Integer,
        db.ForeignKey("quizzes.id"),
        nullable=False,
    )

    score = db.Column(
        db.Float,
        default=0,
    )

    passed = db.Column(
        db.Boolean,
        default=False,
    )

    submitted_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
    )

    enrollment = db.relationship(
        "Enrollment",
        backref=db.backref(
            "quiz_attempts",
            lazy=True,
            cascade="all, delete-orphan",
        ),
    )

    quiz = db.relationship(
        "Quiz",
        backref=db.backref(
            "attempts",
            lazy=True,
            cascade="all, delete-orphan",
        ),
    )