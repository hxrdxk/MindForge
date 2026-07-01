import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "mindforge-development-secret"
    )

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" +
        os.path.join(BASE_DIR, "instance", "mindforge.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PROJECT_NAME = "MindForge"

    PROJECT_TAGLINE = "Forging Minds. Building Futures."

    PROJECT_DESCRIPTION = (
        "AI-powered CS Fundamentals Learning Platform."
    )

    PROJECT_AUTHOR = "Team MindForge"

    LOGO_PATH = "logo/mindforge-logo.png"

    FAVICON = "logo/favicon.png"