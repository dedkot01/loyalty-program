import config

from database import db_session, init_db

from flask import Flask, redirect, render_template, request

from flask_login import LoginManager, current_user, login_required, login_user, logout_user

from models import LoyaltyProgram, Member, User

import rules_access

from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = config.secret_key

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


@app.route('/admin_system/users')
@login_required
def admin_system_users():
    if current_user.is_have_access(rules_access.admin_system_page.access_groups,
                                   how=rules_access.admin_system_page.how):
        users = User.query.all()

        return render_template('admin_system/users/users.html', users=users)
    else:
        return redirect('/admin_system')


@app.route('/admin_system/users/<int:user_id>')
@login_required
def admin_system_user_info(user_id: int):
    if current_user.is_have_access(rules_access.admin_system_page.access_groups,
                                   how=rules_access.admin_system_page.how):
        user = User.query.filter(User.id == user_id).first()

        return render_template('admin_system/users/user_info.html', user=user)
    else:
        return redirect('/admin_system')


@app.route('/admin_system/users/<int:user_id>/edit')
@login_required
def admin_system_user_edit(user_id: int):
    if current_user.is_have_access(rules_access.admin_system_page.access_groups,
                                   how=rules_access.admin_system_page.how):
        user = User.query.filter(User.id == user_id).first()

        return render_template('admin_system/users/user_edit.html', user=user, access_groups=rules_access.access_groups)
    else:
        return redirect('/admin_system')


@app.route('/admin_system/users/<int:user_id>/edit', methods=['POST'])
@login_required
def admin_system_user_edit_post(user_id: int):
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

        db_session.add(user)
        db_session.commit()

        return redirect('/admin_system/users')
    else:
        return redirect('/admin_system')


@app.route('/admin_system/users/<int:user_id>/delete')
@login_required
def admin_system_user_delete(user_id: int):
    if current_user.is_have_access(rules_access.admin_system_page.access_groups,
                                   how=rules_access.admin_system_page.how):
        user = User.query.filter(User.id == user_id).first()

        db_session.delete(user)
        db_session.commit()

        return redirect('/admin_system/users')
    else:
        return redirect('/admin_system')


@app.route('/administrator')
@login_required
def administrator():
    if current_user.is_have_access(rules_access.administrator_page.access_groups,
                                   how=rules_access.administrator_page.how):
        return render_template('administrator/index.html', rules_access=rules_access)
    else:
        return redirect('/')


@app.route('/administrator/loyalty_program/members')
@login_required
def loyalty_program_members():
    if current_user.is_have_access(rules_access.administrator_page.access_groups,
                                   how=rules_access.administrator_page.how):
        members: list = db_session.query(Member).all()
        members = sorted(members, key=lambda member: member.loyalty_program.count, reverse=True)

        return render_template('administrator/loyalty_program/members.html', members=members, rules_access=rules_access)
    else:
        return redirect('/')


@app.route('/administrator/loyalty_program/members/<int:member_id>')
@login_required
def loyalty_program_member(member_id: int):
    member = Member.query.filter(Member.id == member_id).first()

    return render_template('administrator/loyalty_program/member_info.html', member=member)


@app.route('/administrator/loyalty_program/new_member')
@login_required
def loyalty_program_new_member():
    if current_user.is_have_access(rules_access.administrator_page.access_groups,
                                   how=rules_access.administrator_page.how):
        return render_template('administrator/loyalty_program/new_member.html')
    else:
        return redirect('/')


@app.route('/administrator/loyalty_program/new_member', methods=['POST'])
@login_required
def loyalty_program_new_member_post():
    if current_user.is_have_access(rules_access.administrator_page.access_groups,
                                   how=rules_access.administrator_page.how):
        member = Member(
            request.form.get('last_name'),
            request.form.get('first_name'),
            request.form.get('phone'),
            request.form.get('comment'),
        )
        member.loyalty_program = LoyaltyProgram()

        db_session.add(member)
        db_session.commit()

        return render_template('administrator/loyalty_program/member_info.html', member=member)
    else:
        return redirect('/')


@app.route('/administrator/loyalty_program/members/<int:member_id>/edit')
@login_required
def loyalty_program_member_edit(member_id: int):
    if current_user.is_have_access(rules_access.administrator_loyalty_program_member_extends_funcs.access_groups,
                                   how=rules_access.administrator_loyalty_program_member_extends_funcs.how):
        member = Member.query.filter(Member.id == member_id).first()
        return render_template('administrator/loyalty_program/member_edit.html', member=member)
    else:
        return redirect('/administrator/loyalty_program/members')


@app.route('/administrator/loyalty_program/members/<int:member_id>/edit', methods=['POST'])
@login_required
def loyalty_program_member_edit_post(member_id: int):
    if current_user.is_have_access(rules_access.administrator_loyalty_program_member_extends_funcs.access_groups,
                                   how=rules_access.administrator_loyalty_program_member_extends_funcs.how):
        member: Member = Member.query.filter(Member.id == member_id).first()

        member.last_name = request.form.get('last_name')
        member.first_name = request.form.get('first_name')
        member.phone = request.form.get('phone')
        member.comment = request.form.get('comment')
        member.loyalty_program.count = request.form.get('count')

        db_session.add(member)
        db_session.commit()

        return redirect(f'/administrator/loyalty_program/members/{member.id}')
    else:
        return redirect('/administrator/loyalty_program/members')


@app.route('/administrator/loyalty_program/members/<int:member_id>/delete')
@login_required
def loyalty_program_member_delete(member_id: int):
    if current_user.is_have_access(rules_access.administrator_loyalty_program_member_extends_funcs.access_groups,
                                   how=rules_access.administrator_loyalty_program_member_extends_funcs.how):
        member = Member.query.filter(Member.id == member_id).first()
        db_session.delete(member)
        db_session.commit()

    return redirect('/administrator/loyalty_program/members')


@app.route('/administrator/loyalty_program/tag_a_member')
@login_required
def loyalty_program_tag_a_member():
    if current_user.is_have_access(rules_access.administrator_page.access_groups,
                                   how=rules_access.administrator_page.how):
        members: list = db_session.query(Member).all()

        return render_template('administrator/loyalty_program/tag_a_member.html', members=members)
    else:
        return redirect('/')


@app.route('/administrator/loyalty_program/tag_a_member', methods=['POST'])
@login_required
def loyalty_program_tag_a_member_post():
    if current_user.is_have_access(rules_access.administrator_page.access_groups,
                                   how=rules_access.administrator_page.how):
        member_id = request.form.get('member_info')

        member = Member.query.filter(Member.id == member_id).first()
        member.loyalty_program.count += 1

        db_session.add(member)
        db_session.commit()

        return render_template('administrator/loyalty_program/member_info.html', member=member)
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
