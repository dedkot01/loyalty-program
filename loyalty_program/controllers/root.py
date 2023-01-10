from database import db_session

from flask import Blueprint, redirect, render_template, request

from flask_login import current_user, login_required, login_user, logout_user

from models import User

import rules_access

from werkzeug.security import check_password_hash, generate_password_hash

root = Blueprint('root', __name__, template_folder='templates')


@root.route('/registration')
def registration():
    return render_template('registration.html')


@root.route('/registration', methods=['POST'])
def registration_post():
    login = request.form.get('login')
    password = request.form.get('password')
    hash_password = generate_password_hash(password)

    user = User(login, hash_password)
    db_session.add(user)
    db_session.commit()

    return redirect('/')


@root.route('/login')
def login():
    return render_template('login.html')


@root.route('/login', methods=['POST'])
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


@root.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@root.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@root.route('/')
def index():
    return render_template('index.html', rules_access=rules_access)


@root.route('/admin_system')
@login_required
def admin_system():
    if current_user.is_have_access(rules_access.admin_system_page.access_groups,
                                   how=rules_access.admin_system_page.how):
        return render_template('admin_system/index.html')
    else:
        return redirect('/')


@root.route('/administrator')
@login_required
def administrator():
    if current_user.is_have_access(rules_access.administrator_page.access_groups,
                                   how=rules_access.administrator_page.how):
        return render_template('administrator/index.html', rules_access=rules_access)
    else:
        return redirect('/')
