from database import db_session, init_db

from flask import Flask, render_template

from models import User

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
