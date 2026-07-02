from datetime import datetime

from extensions import db


class Enrollment(db.Model):

    __tablename__ = "enrollments"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id"),
        nullable=False,
    )

    progress = db.Column(
        db.Float,
        default=0.0,
    )

    completed = db.Column(
        db.Boolean,
        default=False,
    )

    enrolled_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
    )

    user = db.relationship(
        "User",
        backref=db.backref(
            "enrollments",
            lazy=True,
            cascade="all, delete-orphan",
        ),
    )

    course = db.relationship(
        "Course",
        backref=db.backref(
            "enrollments",
            lazy=True,
            cascade="all, delete-orphan",
        ),
    )

    def __repr__(self):

        return (
            f"<Enrollment "
            f"{self.user_id} -> {self.course_id}>"
        )