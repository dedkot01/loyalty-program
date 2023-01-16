from datetime import datetime, timedelta

from database import db_session

from flask import Blueprint, flash, redirect, render_template, request

from flask_login import current_user, login_required

from models import LoyaltyProgram, Member

import rules_access

loyalty_program = Blueprint('loyalty_program', __name__)


@loyalty_program.route('/members')
@login_required
def members():
    if current_user.is_have_access(rules_access.administrator_page.access_groups,
                                   how=rules_access.administrator_page.how):
        members: list = db_session.query(Member).all()
        members = sorted(members, key=lambda member: member.loyalty_program.count, reverse=True)

        return render_template('administrator/loyalty_program/members.html', members=members, rules_access=rules_access)
    else:
        return redirect('/')


@loyalty_program.route('/members/<int:member_id>')
@login_required
def member(member_id: int):
    member = Member.query.filter(Member.id == member_id).first()

    return render_template('administrator/loyalty_program/member_info.html', member=member)


@loyalty_program.route('/new_member')
@login_required
def new_member():
    if current_user.is_have_access(rules_access.administrator_page.access_groups,
                                   how=rules_access.administrator_page.how):
        return render_template('administrator/loyalty_program/new_member.html')
    else:
        return redirect('/')


@loyalty_program.route('/new_member', methods=['POST'])
@login_required
def new_member_post():
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


@loyalty_program.route('/members/<int:member_id>/edit')
@login_required
def member_edit(member_id: int):
    if current_user.is_have_access(rules_access.administrator_loyalty_program_member_extends_funcs.access_groups,
                                   how=rules_access.administrator_loyalty_program_member_extends_funcs.how):
        member = Member.query.filter(Member.id == member_id).first()
        return render_template('administrator/loyalty_program/member_edit.html', member=member)
    else:
        return redirect('/administrator/loyalty_program/members')


@loyalty_program.route('/members/<int:member_id>/edit', methods=['POST'])
@login_required
def member_edit_post(member_id: int):
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


@loyalty_program.route('/members/<int:member_id>/delete')
@login_required
def member_delete(member_id: int):
    if current_user.is_have_access(rules_access.administrator_loyalty_program_member_extends_funcs.access_groups,
                                   how=rules_access.administrator_loyalty_program_member_extends_funcs.how):
        member = Member.query.filter(Member.id == member_id).first()
        db_session.delete(member)
        db_session.commit()

    return redirect('/administrator/loyalty_program/members')


@loyalty_program.route('/tag_a_member')
@login_required
def tag_a_member():
    if current_user.is_have_access(rules_access.administrator_page.access_groups,
                                   how=rules_access.administrator_page.how):
        members: list = db_session.query(Member).all()

        return render_template('administrator/loyalty_program/tag_a_member.html', members=members)
    else:
        return redirect('/')


@loyalty_program.route('/tag_a_member', methods=['POST'])
@login_required
def tag_a_member_post():
    if current_user.is_have_access(rules_access.administrator_page.access_groups,
                                   how=rules_access.administrator_page.how):
        member_id = request.form.get('member_info')

        member = Member.query.filter(Member.id == member_id).first()

        if datetime.utcnow() > member.loyalty_program.time_mark + timedelta(seconds=20):
            member.loyalty_program.count += 1
            member.loyalty_program.time_mark = datetime.utcnow()

            db_session.add(member)
            db_session.commit()
        else:
            flash('Гостя уже не так давно отмечали')

        return render_template('administrator/loyalty_program/member_info.html', member=member)
    else:
        return redirect('/')
