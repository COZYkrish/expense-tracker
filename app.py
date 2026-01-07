from flask import Flask, redirect
from flask_login import current_user
from config import Config
from extensions import db, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Import blueprints
    from routes.auth import auth_bp
    from routes.user import user_bp
    from routes.admin import admin_bp
    from routes.analytics import analytics_bp

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(analytics_bp)

    # Root route
    @app.route("/")
    def home():
        if current_user.is_authenticated:
            if current_user.role == "admin":
                return redirect("/admin")
            return redirect("/user")
        return redirect("/auth/login")

    return app


# Create app instance
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
