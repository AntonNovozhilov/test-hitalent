from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src.core.db import Base


class User(Base):
    """Пользователь"""
    
    username = Column(String(), unique=True, nullable=False)
    hash_password = Column(String(), nullable=False)

    answers = relationship(
        "Answer", back_populates="user", cascade="all, delete-orphan"
    )
