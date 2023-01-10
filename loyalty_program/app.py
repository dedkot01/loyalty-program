import config

from controllers.loyalty_program import loyalty_program
from controllers.users import users

from database import db_session, init_db

from flask import Flask, redirect, render_template, request

from flask_login import LoginManager, current_user, login_required, login_user, logout_user

from models import User

import rules_access

from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = config.secret_key

app.register_blueprint(users, url_prefix='/admin_system/users')
app.register_blueprint(loyalty_program, url_prefix='/administrator/loyalty_program')

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == user_id).first()


@app.route('/registration')
def registration():
    return render_template('registration.html')


@app.route('/registration', methods=['POST'])
def registration_post():
    login = request.form.get('login')
    password = request.form.get('password')
    hash_password = generate_password_hash(password)

    user = User(login, hash_password)
    db_session.add(user)
    db_session.commit()

    return redirect('/')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    login = request.form.get('login')
    password = request.form.get('password')

    user = User.query.filter(User.login == login).first()

    if user is None:
        return redirect('/login')
    else:
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect(request.args.get('next') or '/')
        else:
            return redirect('/login')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/')
def index():
    return render_template('index.html', rules_access=rules_access)


@app.route('/admin_system')
@login_required
def admin_system():
    if current_user.is_have_access(rules_access.admin_system_page.access_groups,
                                   how=rules_access.admin_system_page.how):
        return render_template('admin_system/index.html')
    else:
        return redirect('/')


@app.route('/administrator')
@login_required
def administrator():
    if current_user.is_have_access(rules_access.administrator_page.access_groups,
                                   how=rules_access.administrator_page.how):
        return render_template('administrator/index.html', rules_access=rules_access)
    else:
        return redirect('/')


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


def main(
    host: str,
    port: int,
    debug: bool,
):
    init_db()
    create_admin_user()

    app.run(
        host=host,
        port=port,
        debug=debug,
    )


if __name__ == "__main__":
    from arguments import get_args

    args = get_args()
    main(
        host=args.host,
        port=args.port,
        debug=args.debug,
    )
