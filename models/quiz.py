from datetime import datetime

from extensions import db


class Quiz(db.Model):

    __tablename__ = "quizzes"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    module_id = db.Column(
        db.Integer,
        db.ForeignKey("modules.id"),
        nullable=False,
        unique=True,
    )

    title = db.Column(
        db.String(200),
        nullable=False,
    )

    description = db.Column(
        db.Text,
        default="",
    )

    passing_score = db.Column(
        db.Integer,
        default=70,
    )

    is_published = db.Column(
        db.Boolean,
        default=False,
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
    )

    module = db.relationship(
        "Module",
        back_populates="quiz",
    )

    def __repr__(self):

        return f"<Quiz {self.title}>"