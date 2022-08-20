from database import Base

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    last_name = Column(String(50), unique=False)
    first_name = Column(String(50), unique=False)
    phone = Column(String(120), unique=False)

    loyalty_program = relationship('LoyaltyProgram', back_populates='users', uselist=False)

    def __init__(self, last_name: str, first_name: str, phone: str) -> None:
        self.last_name = last_name
        self.first_name = first_name
        self.phone = phone

    def __repr__(self):
        return f'<User {self.last_name!r} {self.first_name!r} - {self.phone!r}>'


class LoyaltyProgram(Base):
    __tablename__ = 'loyalty_program'

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    count = Column(Integer, unique=False)

    users = relationship('User', back_populates='loyalty_program')

    def __init__(self, count: int = 1) -> None:
        self.count = count

    def __repr__(self):
        return f'<LoyaltyProgram {self.count!r}>'
