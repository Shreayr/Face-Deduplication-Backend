from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey

from datetime import datetime, UTC

from database import Base


#USERS TABLE

class User(Base):#Store data in the database.

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False)

    password = Column(String, nullable=False)

    role = Column(String, default="client")

    is_active = Column(Boolean, default=True)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC)
    )


#UPLOADED IMAGES TABLE 

class UploadedImage(Base):

    __tablename__ = "uploaded_images"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String, nullable=False)

    filepath = Column(String, nullable=False)

    uploaded_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC)
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )