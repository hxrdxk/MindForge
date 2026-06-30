import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:

    PROJECT_NAME = "MindForge"

    PROJECT_TAGLINE = "Forging Minds. Building Futures."

    PROJECT_DESCRIPTION = (
        "An AI-powered Computer Science learning platform."
    )

    PROJECT_AUTHOR = "Team MindForge"

    LOGO_PATH = "logo/mindforge-logo.png"

    FAVICON = "logo/favicon.png"
        
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "mindforge-development-secret-key"
    )

    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{os.path.join(BASE_DIR,'instance','app.db')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False