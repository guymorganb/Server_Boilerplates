from datetime import datetime
from app.db import Base
from .Vote import Vote
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, select, func
from sqlalchemy.orm import relationship, column_property


# Remember that we write SQLAlchemy models as Python classes.


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    post_url = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    vote_count = column_property(
        select(func.count(Vote.id)).where(Vote.post_id == id)
    )  # dynamic property
    # When we query the model, this dynamic property will perform a SELECT,
    # together with the SQLAlchemy func.count() method, to add up the votes.
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    user = relationship('User')

    comments = relationship('Comment', cascade='all,delete')
    votes = relationship('Vote', cascade='all,delete')
# The Post model includes a dynamic property for votes,
# meaning that a query for a post should also return information about the number of votes the post has
# Add the following line to the Post class:votes = relationship('Vote', cascade='all,delete')
# In MySQL, an ON DELETE CASCADE statement deletes the corresponding foreign key records
# when a record from the specified table is deleted.
# In this case, deleting a post from the database also deletes all its associated comments.

