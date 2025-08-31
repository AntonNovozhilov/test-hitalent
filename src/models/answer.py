from sqlalchemy import Column, ForeignKey, Text, UUID
from sqlalchemy.orm import relationship
from src.core.db import Base


class Answer(Base):
    """Ответы"""

    question_id = Column(
        UUID(as_uuid=True),
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    text = Column(Text, nullable=False)

    question = relationship("Question", back_populates="answers")
    user = relationship("User", back_populates="answers")
