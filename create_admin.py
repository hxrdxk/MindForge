from app import app
from extensions import db
from models.user import User

with app.app_context():

    existing = User.query.filter_by(
        email="admin@mindforge.com"
    ).first()

    if existing:

        print("Admin already exists.")

    else:

        admin = User(
            full_name="Administrator",
            email="admin@mindforge.com",
            role="admin",
        )

        admin.set_password("admin123")

        db.session.add(admin)
        db.session.commit()

        print("Admin created successfully.")