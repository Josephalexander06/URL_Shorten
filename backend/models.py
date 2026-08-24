from utils.database import Base
from sqlalchemy import Column,Integer,String,TIMESTAMP,text


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer,primary_key=True,nullable=False)
    original_url = Column(String,nullable=False)
    shorten_url = Column(String,nullable=False,unique=True,index=True)
    count = Column(Integer)
    ip_address = Column(String)
    user_agent_info = Column(String)
    access_at = Column(TIMESTAMP(timezone=True),server_default=text("now()"))
    expire_at = Column(TIMESTAMP(timezone=True))
    created_at = Column(TIMESTAMP(timezone=True),server_default=text('now()'))

