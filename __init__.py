from datetime import datetime

from flask import Flask

from config import Config
from extensions import db, migrate, login_manager
from models.user import User

def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):

        return db.session.get(User, int(user_id))
    
    from routes.main import main_bp
    app.register_blueprint(main_bp)

    from routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from routes.student import student_bp
    app.register_blueprint(student_bp)

    from routes.teacher import teacher_bp
    app.register_blueprint(teacher_bp)

    from routes.course import course_bp
    app.register_blueprint(course_bp)

    from routes.enrollment import enrollment_bp
    app.register_blueprint(enrollment_bp)

    from routes.teacher_lessons import teacher_lessons_bp
    app.register_blueprint(teacher_lessons_bp)

    from routes.teacher_quiz import teacher_quiz_bp
    app.register_blueprint(teacher_quiz_bp)

    @app.context_processor
    def inject_brand():
        return {
            "brand": {
                "name": app.config["PROJECT_NAME"],
                "tagline": app.config["PROJECT_TAGLINE"],
                "description": app.config["PROJECT_DESCRIPTION"],
                "author": app.config["PROJECT_AUTHOR"],
                "logo": app.config["LOGO_PATH"],
                "favicon": app.config["FAVICON"],
            },
            "current_year": datetime.now().year,
        }

    return app