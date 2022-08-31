import config

from database import db_session, init_db

from flask import Flask, redirect, render_template, request

from flask_login import LoginManager, login_required, login_user

from models import LoyaltyProgram, Member, User

from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = config.secret_key

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == user_id).first()


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    login = request.form.get('login')
    password = request.form.get('password')

    user = User.query.filter(User.login == login).first()

    if user is None:
        print(f'Пользователь "{login}" не найден')
        return redirect('/login')
    else:
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect('/')
        else:
            print('Неверный пароль')
            return redirect('/login')


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

    print(f'Пользователь "{login}" зарегистрирован')

    return redirect('/')


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/administrator')
@login_required
def administrator():
    return render_template('administrator/index.html')


@app.route('/administrator/loyalty_program/members')
def loyalty_program_members():
    members: list = db_session.query(Member).all()
    members = sorted(members, key=lambda member: member.loyalty_program.count, reverse=True)

    return render_template('administrator/loyalty_program/members.html', members=members)


@app.route('/administrator/loyalty_program/tag_a_member')
def loyalty_program_tag_a_member():
    members: list = db_session.query(Member).all()

    return render_template('administrator/loyalty_program/tag_a_member.html', members=members)


@app.route('/administrator/loyalty_program/tag_a_member', methods=['POST'])
def loyalty_program_tag_a_member_post():
    member_id = request.form.get('member_info')

    member = Member.query.filter(Member.id == member_id).first()
    member.loyalty_program.count += 1

    db_session.add(member)
    db_session.commit()

    return render_template('administrator/loyalty_program/member_info.html', member=member)


@app.route('/administrator/loyalty_program/new_member')
def loyalty_program_new_member():
    return render_template('administrator/loyalty_program/new_member.html')


@app.route('/administrator/loyalty_program/new_member', methods=['POST'])
def loyalty_program_new_member_post():
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


def main(
    port: int,
    debug: bool,
):
    init_db()

    app.run(
        port=port,
        debug=debug,
    )


if __name__ == "__main__":
    from arguments import get_args

    args = get_args()
    main(
        port=args.port,
        debug=args.debug,
    )
