from datetime import datetime

from extensions import db


class LessonProgress(db.Model):

    __tablename__ = "lesson_progress"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    enrollment_id = db.Column(
        db.Integer,
        db.ForeignKey("enrollments.id"),
        nullable=False,
    )

    lesson_id = db.Column(
        db.Integer,
        db.ForeignKey("lessons.id"),
        nullable=False,
    )

    completed = db.Column(
        db.Boolean,
        default=False,
    )

    completed_at = db.Column(
        db.DateTime,
    )

    enrollment = db.relationship(
        "Enrollment",
        backref=db.backref(
            "lesson_progress",
            lazy=True,
            cascade="all, delete-orphan",
        ),
    )

    lesson = db.relationship(
        "Lesson",
        backref=db.backref(
            "lesson_progress",
            lazy=True,
        ),
    )

    __table_args__ = (
        db.UniqueConstraint(
            "enrollment_id",
            "lesson_id",
            name="uq_enrollment_lesson",
        ),
    )
    
    def mark_complete(self):

        self.completed = True
        self.completed_at = datetime.utcnow()