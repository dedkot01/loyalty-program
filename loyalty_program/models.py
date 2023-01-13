from datetime import datetime

from database import Base

from flask_login import UserMixin

from sqlalchemy import ARRAY, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login = Column(String(25), unique=True)
    password = Column(String(255))
    access_groups = Column(ARRAY(String))

    def __init__(self, login: str, password: str, access_groups: list = None):
        self.login = login
        self.password = password
        self.access_groups = [] if access_groups is None else access_groups

    def is_have_access(self, access_groups: list, how='any'):
        if 'admin' in self.access_groups:
            return True

        compare_result = [True if access_group in access_groups else False for access_group in self.access_groups]
        if how == 'any':
            return any(compare_result)
        elif how == 'all':
            return all(compare_result)
        else:
            raise Exception(f'Method "{how}" not implemented. Expected: "any" or "all".')


class Member(Base):
    __tablename__ = 'members'

    id = Column(Integer, primary_key=True)
    last_name = Column(String(50))
    first_name = Column(String(50))
    phone = Column(String(120))
    comment = Column(String(255))

    loyalty_program = relationship(
        'LoyaltyProgram',
        cascade="all, delete-orphan", single_parent=True,
        back_populates='members', uselist=False)

    def __init__(self, last_name: str, first_name: str, phone: str, comment: str) -> None:
        self.last_name = last_name
        self.first_name = first_name
        self.phone = phone
        self.comment = comment

    def __repr__(self):
        return f'<Member {self.last_name!r} {self.first_name!r} - {self.phone!r}>'


class LoyaltyProgram(Base):
    __tablename__ = 'loyalty_program'

    id = Column(Integer, ForeignKey('members.id'), primary_key=True)
    count = Column(Integer)
    time_mark = Column(DateTime)

    members = relationship('Member', back_populates='loyalty_program')

    def __init__(self, count: int = 1, time_mark: datetime = datetime.utcnow()) -> None:
        self.count = count
        self.time_mark = time_mark

    def __repr__(self):
        return f'<LoyaltyProgram {self.count!r}>'
