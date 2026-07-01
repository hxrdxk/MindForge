from functools import wraps

from flask import flash
from flask import redirect
from flask import url_for

from flask_login import (
    current_user,
)


def role_required(*roles):

    def decorator(view):

        @wraps(view)
        def wrapped(*args, **kwargs):

            if not current_user.is_authenticated:

                return redirect(
                    url_for("auth.login")
                )

            if current_user.role not in roles:

                flash(
                    "You are not authorized to access this page.",
                    "danger",
                )

                return redirect(
                    url_for("main.home")
                )

            return view(*args, **kwargs)

        return wrapped

    return decorator


def student_required(view):

    return role_required("student")(view)


def teacher_required(view):

    return role_required("teacher")(view)


def admin_required(view):

    return role_required("admin")(view)