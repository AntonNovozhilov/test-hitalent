from sqlalchemy import Column, Text
from sqlalchemy.orm import relationship

from src.core.db import Base


class Question(Base):
    """Вопросы"""
    
    text = Column(Text, nullable=False)

    answers = relationship(
        "Answer", back_populates="question", cascade="all, delete-orphan"
    )
