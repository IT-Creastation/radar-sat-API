from sqlalchemy import Column, ForeignKey, Integer, String, Boolean

from sqlalchemy.orm import relationship

from DB.database import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, unique=True)
    name = Column(String, unique=True)
    is_downloaded = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="images")
