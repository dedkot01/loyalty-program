from database import Base

from flask_login import UserMixin

from sqlalchemy import ARRAY, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login = Column(String(25), unique=True)
    password = Column(String(255))
    access_groups = Column(ARRAY(String))

    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password


class Member(Base):
    __tablename__ = 'members'

    id = Column(Integer, primary_key=True)
    last_name = Column(String(50))
    first_name = Column(String(50))
    phone = Column(String(120))
    comment = Column(String(255))

    loyalty_program = relationship('LoyaltyProgram', back_populates='members', uselist=False)

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

    members = relationship('Member', back_populates='loyalty_program')

    def __init__(self, count: int = 1) -> None:
        self.count = count

    def __repr__(self):
        return f'<LoyaltyProgram {self.count!r}>'
