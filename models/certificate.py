from datetime import datetime

from extensions import db


class Certificate(db.Model):

    __tablename__ = "certificates"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    certificate_id = db.Column(
        db.String(30),
        unique=True,
        nullable=False,
    )

    enrollment_id = db.Column(
        db.Integer,
        db.ForeignKey("enrollments.id"),
        nullable=False,
        unique=True,
    )

    issued_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
    )

    final_score = db.Column(
        db.Float,
        default=0,
    )

    enrollment = db.relationship(
        "Enrollment",
        backref=db.backref(
            "certificate",
            uselist=False,
            cascade="all, delete-orphan",
        ),
    )

    def __repr__(self):

        return (
            f"<Certificate "
            f"{self.certificate_id}>"
        )