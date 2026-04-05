from flask import Flask

from blog_app.database import Base, SessionLocal, engine
from blog_app.routes import register_routes
from blog_app.seed_data import seed_database


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")

    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        seed_database(session)

    register_routes(app)
    return app
