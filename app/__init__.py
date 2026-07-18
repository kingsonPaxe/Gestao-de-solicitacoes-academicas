import os
from flask import Flask
from .config import Config
from .database import db, login_manager, csrf, migrate


def create_app(config_class: type = Config) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    os.makedirs(app.instance_path, exist_ok=True)
    upload_dir = os.path.join(app.root_path, "static", "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    app.config["UPLOAD_FOLDER"] = upload_dir

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Faça login para continuar."
    login_manager.login_message_category = "warning"

    from .models.user import Usuario

    @login_manager.user_loader
    def load_user(user_id: str):
        return db.session.get(Usuario, int(user_id))

    # Blueprints
    from .routes.auth import auth_bp
    from .routes.main import main_bp
    from .routes.aluno import aluno_bp
    from .routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(aluno_bp, url_prefix="/aluno")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # Error handlers
    from .utils.errors import register_error_handlers
    register_error_handlers(app)

    with app.app_context():
        db.create_all()
        from .utils.seed import run_seed
        run_seed()

    return app
