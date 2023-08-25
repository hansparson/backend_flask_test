
import datetime
from .db import Column, PkModel, db
from sqlalchemy.sql import text
from sqlalchemy.orm import validates
import enum

class UserLogStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    LOCK = "LOCK"
    DELETED = "DELETED"

class Users(PkModel):

    __tablename__ = "user"
    
    status = Column(db.Enum(UserLogStatus), nullable=False, server_default='ACTIVE')
    email = Column(db.String(), nullable=True, default='')
    first_name = Column(db.String(), nullable=True, default='')
    last_name = Column(db.String(), nullable=True, default='')
    avatar = Column(db.String(), nullable=True, default='')
    created_at = Column(db.DateTime(), server_default=text("now()"))
    updated_at = Column(db.DateTime(), onupdate=text("now()"))
    deleted_at = Column(db.DateTime())
    
    @validates('status')
    def validate_status(self, key, value):
        if value == UserLogStatus.DELETED:
            self.deleted_at = datetime.datetime.now()
        return value

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        if commit:
            return self.save()
        return self

    def save(self, commit=True):
        """Save the record."""
        try:
            db.session.add(self)
            if commit:
                db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return False
        return self
    
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def delete(self, commit: bool = True) -> None:
        """Remove the record from the database."""
        try:
            db.session.delete(self)
            if commit:
                return db.session.commit()
        except Exception:
            db.session.rollback()
        return
    
    def __repr__(self):
        """Represent instance as a unique string."""
        return f"{self.id}"

class db_users_query(object):
    @staticmethod
    def get_user_by_id(id):
        order = Users.query.filter(Users.id == id).filter(Users.status == 'ACTIVE').first()
        return order
    
    @staticmethod
    def get_all_users():
        order = Users.query.filter(Users.status == 'ACTIVE')
        return order
    
    @staticmethod
    def delete_user(id, status):
        order = Users.query.filter(Users.id == id).filter(Users.status == 'ACTIVE').first().update(
            status=status, 
            deleted_at=datetime.datetime.now())
        return order
    
    @staticmethod
    def update_user_data(id, email, first_name, last_name, avatar):
        order = Users.query.filter(Users.id == id).filter(Users.status == 'ACTIVE').first().update(
            email=email,
            first_name=first_name,
            last_name=last_name,
            avatar=avatar)
        return order