import config

from controllers.loyalty_program import loyalty_program
from controllers.root import root
from controllers.users import users

from database import db_session, init_db

from flask import Flask

from flask_login import LoginManager

from models import User

from werkzeug.security import generate_password_hash


def create_app():
    app = Flask(__name__)
    app.secret_key = config.secret_key

    app.register_blueprint(root)
    app.register_blueprint(users, url_prefix='/admin_system/users')
    app.register_blueprint(loyalty_program, url_prefix='/administrator/loyalty_program')

    login_manager = LoginManager(app)
    login_manager.login_view = 'root.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == user_id).first()

    def create_admin_user():
        if User.query.filter(User.login == config.admin_login).first() is None:
            admin = User(
                login=config.admin_login,
                password=generate_password_hash(config.admin_password),
                access_groups=['admin'],
            )
            db_session.add(admin)
            db_session.commit()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    init_db()
    create_admin_user()

    return app


if __name__ == "__main__":
    from arguments import get_args

    args = get_args()
    app = create_app()
    app.run(
        host=args.host,
        port=args.port,
        debug=args.debug,
    )
