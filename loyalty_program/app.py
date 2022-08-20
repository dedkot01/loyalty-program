from database import db_session, init_db

from flask import Flask, render_template, request

from models import LoyaltyProgram, User

app = Flask(__name__)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/administrator')
def administrator():
    return render_template('administrator/index.html')


@app.route('/administrator/loyalty_program')
def loyalty_program():
    users: list = db_session.query(User).all()

    return render_template('administrator/loyalty_program.html', users=users)


@app.route('/administrator/loyalty_program', methods=['POST'])
def loyalty_program_post():
    last_name = request.form.get('last_name')
    first_name = request.form.get('first_name')
    phone = request.form.get('phone')

    u = User.query.filter(User.last_name == last_name,
                          User.first_name == first_name,
                          User.phone == phone,).first()

    if u is None:
        u = User(last_name, first_name, phone)
        u.loyalty_program = LoyaltyProgram()
    else:
        u.loyalty_program.count += 1
    db_session.add(u)
    db_session.commit()

    return str(u.loyalty_program.count)


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
