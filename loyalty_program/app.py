from database import db_session, init_db

from flask import Flask, render_template, request

from models import LoyaltyProgram, Member

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
