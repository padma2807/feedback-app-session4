from sqlalchemy import Column, Integer, String, Text
from .database import Base
from pydantic import BaseModel, EmailStr, Field

# SQLAlchemy Model
class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    rating = Column(Integer)
    experience = Column(Text)

# Pydantic Schema
class FeedbackCreate(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    rating: int = Field(..., ge=1, le=5)
    experience: str = Field(..., min_length=1)
