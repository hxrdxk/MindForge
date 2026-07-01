from datetime import datetime

from extensions import db


class Course(db.Model):

    __tablename__ = "courses"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    title = db.Column(
        db.String(200),
        nullable=False,
    )

    slug = db.Column(
        db.String(200),
        unique=True,
        nullable=False,
    )

    description = db.Column(
        db.Text,
        nullable=False,
    )

    category = db.Column(
        db.String(100),
        nullable=False,
    )

    difficulty = db.Column(
        db.String(50),
        default="Beginner",
    )

    thumbnail = db.Column(
        db.String(255),
    )

    duration = db.Column(
        db.String(50),
        default="0 Hours",
    )

    language = db.Column(
        db.String(50),
        default="English",
    )

    instructor = db.Column(
        db.String(120),
        default="MindForge",
    )

    is_published = db.Column(
        db.Boolean,
        default=False,
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    def __repr__(self):

        return f"<Course {self.title}>"