# from models.connection import Base
from sqlalchemy import Column, Integer, String

from models.connection import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    fullname = Column(String(100))
    nickname = Column(String(100))

    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (
            self.name,
            self.fullname,
            self.nickname,
        )
