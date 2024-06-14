from sqlalchemy import (Boolean, Column, String)
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    """
    Database Model for an application user
    """

    __tablename__ = 'users'

    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    email = Column(String(100), unique=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean(), default=False)

    chatbots = relationship("ChatBot", back_populates="user")
