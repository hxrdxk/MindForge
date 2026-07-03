from extensions import db


class Answer(db.Model):

    __tablename__ = "answers"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    attempt_id = db.Column(
        db.Integer,
        db.ForeignKey("quiz_attempts.id"),
        nullable=False,
    )

    question_id = db.Column(
        db.Integer,
        db.ForeignKey("questions.id"),
        nullable=False,
    )

    selected_option_id = db.Column(
        db.Integer,
        db.ForeignKey("options.id"),
        nullable=False,
    )

    is_correct = db.Column(
        db.Boolean,
        default=False,
    )

    attempt = db.relationship(
        "QuizAttempt",
        backref=db.backref(
            "answers",
            lazy=True,
            cascade="all, delete-orphan",
        ),
    )

    question = db.relationship("Question")

    selected_option = db.relationship("Option")