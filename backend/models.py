from database import Base
from sqlalchemy import Column,Integer,String,TIMESTAMP,text,ForeignKey
from sqlalchemy.orm import relationship


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer,primary_key=True,nullable=False)
    original_url = Column(String,nullable=False)
    shorten_url = Column(String,nullable=False,unique=True,index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    count = Column(Integer)
    ip_address = Column(String)
    user_agent_info = Column(String)
    access_at = Column(TIMESTAMP(timezone=True),server_default=text("now()"))
    expire_at = Column(TIMESTAMP(timezone=True))
    created_at = Column(TIMESTAMP(timezone=True),server_default=text('now()'))

    user = relationship("User",back_populates="urls")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,nullable=False)
    email = Column(String,nullable=False,unique=True,index=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),server_default=text('now()'))


    urls = relationship("URL",back_populates="user")
