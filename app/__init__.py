from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Database object
# Used in whole project
# Connects Python with database
db = SQLAlchemy()

# Migration object
# Handles database changes
migrate=Migrate()

# App factory function
# Creates Flask app
def create_app():
    app=Flask(__name__)
    
    # Secret key for session/flash msg security
    app.config["SECRET_KEY"] = "your-secret-key"

    # SQLite database file
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"

    # Disable unnecessary warnings
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Connect DB with app
    db.__init__(app)
    
    # Connect migrate with app + DB
    migrate.__init__(app,db)

    # Import blueprints
    from app.routes.auth import auth_dp
    from app.routes.tasks import task_dp

    # Register blueprints
    app.register_blueprint(auth_dp)
    app.register_blueprint(task_dp)

    return app
