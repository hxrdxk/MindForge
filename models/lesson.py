from datetime import datetime

from extensions import db


class Lesson(db.Model):

    __tablename__ = "lessons"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    module_id = db.Column(
        db.Integer,
        db.ForeignKey("modules.id"),
        nullable=False,
    )

    title = db.Column(
        db.String(200),
        nullable=False,
    )

    content = db.Column(
        db.Text,
        default="",
    )

    video_url = db.Column(
        db.String(500),
    )

    position = db.Column(
        db.Integer,
        default=1,
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
    )

    module = db.relationship(
        "Module",
        backref=db.backref(
            "lessons",
            lazy=True,
            cascade="all, delete-orphan",
            order_by="Lesson.position",
        ),
    )

    def __repr__(self):

        return f"<Lesson {self.title}>"