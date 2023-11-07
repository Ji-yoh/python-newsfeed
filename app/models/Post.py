from datetime import datetime
from app.db import Base
from .Vote import Vote
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, select, func
from sqlalchemy.orm import relationship, column_property


# create a Post model
class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    post_url = Column(String(500), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    vote_count = column_property(
        select(func.count(Vote.id)).where(Vote.post_id == id) # func.count() did not need to be an array
    )

    # add relationship to User model
    user = relationship('User')
    # add relationship to Comment model
    comments = relationship('Comment', cascade='all,delete')
    # add relationship to Vote model
    votes = relationship('Vote', cascade='all,delete')