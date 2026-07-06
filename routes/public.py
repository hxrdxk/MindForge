from flask import Blueprint, render_template

from models.certificate import Certificate

public_bp = Blueprint(
    "public",
    __name__,
)


@public_bp.route(
    "/verify/<certificate_id>"
)
def verify_certificate(certificate_id):

    certificate = Certificate.query.filter_by(
        certificate_id=certificate_id
    ).first()

    return render_template(
        "public/verify_certificate.html",
        certificate=certificate,
    )