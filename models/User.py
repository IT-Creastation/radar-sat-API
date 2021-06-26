from DB.database import Base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    # TODO: satellite should be an enum instead of String :p
    satellite = Column(String)
    download_image_from = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    cloud_coverage = Column(Integer)

    images = relationship("Image", back_populates="user")
