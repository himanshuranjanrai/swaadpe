from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from backend.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="customer")  # admin / customer


class TiffinStatus(Base):
    __tablename__ = "tiffin_status"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)

    lunch = Column(Boolean, default=False)
    dinner = Column(Boolean, default=False)