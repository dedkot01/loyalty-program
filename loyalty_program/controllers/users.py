from database import db_session

from flask import Blueprint, redirect, render_template, request

from flask_login import current_user, login_required

from models import User

import rules_access

from werkzeug.security import generate_password_hash

users = Blueprint('users', __name__)


@users.route('/')
@login_required
def index():
    if current_user.is_have_access(rules_access.admin_system_page.access_groups,
                                   how=rules_access.admin_system_page.how):
        admin = User.query.filter(User.login == 'admin').first()
        users = User.query.filter(User.login != 'admin').all()

        return render_template('admin_system/users/users.html', admin=admin, users=users)
    else:
        return redirect('/admin_system')


@users.route('/<int:user_id>')
@login_required
def info(user_id: int):
    if current_user.is_have_access(rules_access.admin_system_page.access_groups,
                                   how=rules_access.admin_system_page.how):
        user = User.query.filter(User.id == user_id).first()

        return render_template('admin_system/users/user_info.html', user=user)
    else:
        return redirect('/admin_system')


@users.route('/<int:user_id>/edit')
@login_required
def edit(user_id: int):
    if current_user.is_have_access(rules_access.admin_system_page.access_groups,
                                   how=rules_access.admin_system_page.how):
        user = User.query.filter(User.id == user_id).first()

        return render_template('admin_system/users/user_edit.html', user=user, access_groups=rules_access.access_groups)
    else:
        return redirect('/admin_system')


@users.route('/<int:user_id>/edit', methods=['POST'])
@login_required
def edit_post(user_id: int):
    if current_user.is_have_access(rules_access.admin_system_page.access_groups,
                                   how=rules_access.admin_system_page.how):
        user: User = User.query.filter(User.id == user_id).first()

        user.login = request.form.get('login')
        if request.form.get('is_new_password'):
            new_password = generate_password_hash(request.form.get('password'))
            user.password = new_password

        new_access_groups = []
        for access_group in rules_access.access_groups.keys():
            if request.form.get(access_group):
                new_access_groups.append(access_group)
        user.access_groups = new_access_groups

        try:
            db_session.add(user)
            db_session.commit()
        except Exception as e:
            # TODO alarm in page
            print(e)

        return redirect('/admin_system/users')
    else:
        return redirect('/admin_system')


@users.route('/<int:user_id>/delete')
@login_required
def delete(user_id: int):
    if current_user.is_have_access(rules_access.admin_system_page.access_groups,
                                   how=rules_access.admin_system_page.how):
        user = User.query.filter(User.id == user_id).first()

        # TODO alert in page
        if user.login != 'admin':
            db_session.delete(user)
            db_session.commit()

        return redirect('/admin_system/users')
    else:
        return redirect('/admin_system')
