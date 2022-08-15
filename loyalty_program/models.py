from database import Base

from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    phone = Column(String(120), unique=True)

    def __repr__(self):
        return f'<User {self.name!r}>'
