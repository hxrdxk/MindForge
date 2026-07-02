from extensions import db


class Question(db.Model):

    __tablename__ = "questions"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    quiz_id = db.Column(
        db.Integer,
        db.ForeignKey("quizzes.id"),
        nullable=False,
    )

    question_text = db.Column(
        db.Text,
        nullable=False,
    )

    question_type = db.Column(
        db.String(20),
        default="mcq",
    )

    points = db.Column(
        db.Integer,
        default=1,
    )

    position = db.Column(
        db.Integer,
        default=1,
    )

    quiz = db.relationship(
        "Quiz",
        backref=db.backref(
            "questions",
            lazy=True,
            cascade="all, delete-orphan",
            order_by="Question.position",
        ),
    )

    def __repr__(self):

        return f"<Question {self.id}>"