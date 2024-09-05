from .database import Base
from sqlalchemy import TIMESTAMP, ForeignKey, Integer, Column, String
from sqlalchemy.orm import relationship

class User(Base): 
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    jioned_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=('now()'))


    blog = relationship("Blog", back_populates="owner")
    



class Blog(Base): 
    __tablename__ = 'blog'
    id = Column(Integer, primary_key=True, unique=True)
    title = Column(String, nullable=False)
    s_description = Column(String, nullable=False)
    l_description = Column(String, nullable=False)
    created_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=('now()'))

    owner_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))

    owner = relationship("User", back_populates="blog")
