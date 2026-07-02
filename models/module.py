from datetime import datetime

from extensions import db


class Module(db.Model):

    __tablename__ = "modules"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id"),
        nullable=False,
    )

    title = db.Column(
        db.String(200),
        nullable=False,
    )

    description = db.Column(
        db.Text,
        default="",
    )

    position = db.Column(
        db.Integer,
        default=1,
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
    )

    course = db.relationship(
        "Course",
        backref=db.backref(
            "modules",
            lazy=True,
            cascade="all, delete-orphan",
            order_by="Module.position",
        ),
    )

    quiz = db.relationship(
        "Quiz",
        back_populates="module",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def __repr__(self):

        return f"<Module {self.title}>"