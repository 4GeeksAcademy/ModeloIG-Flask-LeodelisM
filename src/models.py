from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

# Modelo para Usuario

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    firstname: Mapped[str] = mapped_column(String(50), nullable=False)
    lastname: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    
# Relaciones

    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", foreign_keys="Comment.autor_id", back_populates="author")

    def serialize(self):
        return {

            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email

            # do not serialize the password, its a security breach(excluye la contraseña por seguridad)
        }
    
class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey('user.id'))

# Relaciones

    user = relationship("User", back_populates="post")
    media = relationship("Media", back_populates="post")
    comments = relationship("Comment", back_populates="post")

    def serialize(self):
        return {

            "id": self.id,
            "user_id": self.user_id
        }
    

class Comment (db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(200), nullable=False)
    author_id: Mapped[int] = mapped_column(db.ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(db.ForeignKey('post.id'), nullable=False)

# Relaciones

    author = relationship("User", foreign_keys=[author_id], back_populates="comments")
    post = relationship("Post", back_populates="comments")


    def serialize(self):
        return {
            
            "id": self.id,
            "text": self.comment_text,
            "autor_id": self.author_id,
            "post_id": self.post_id
        }


class Follower(db.Model):
    user_from_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"), primary_key=True)
    user_to_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"), primary_key=True)

# Relaciones

    follower = relationship("User", foreign_keys=[user_from_id], back_populates="following")
    following = relationship("User", foreign_keys=[user_to_id], back_populates="followers")

    def serialize(self):
        return {

            "follower_id": self.user_from_id,
            "following_id": self.user_to_id
        
        }

class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    url: Mapped[str] = mapped_column(String(1000), nullable=False)
    post_id: Mapped[int] = mapped_column(db.ForeignKey("post.id"))

# Relaciones

    post = relationship("Post", back_populates="media")

    def serialize(self):
        return {

            "id": self.id,
            "type": self.type,
            "url": self.url,
            "post_id": self.post_id
        }

