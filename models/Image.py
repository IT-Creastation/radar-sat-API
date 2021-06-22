from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..DB.database import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, unique=True)
    name = Column(String, unique=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="images")
