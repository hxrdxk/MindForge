from extensions import db
from .user import User
from .course import Course
from .module import Module
from .enrollment import Enrollment
from .lesson import Lesson

def init_db(app):

    db.init_app(app)

    with app.app_context():
        db.create_all()