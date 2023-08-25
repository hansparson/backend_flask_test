from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from sqlalchemy import DateTime, exc
from typing import Callable
from enum import Enum


# Use the typing to tell the IDE what the type is.
class SQLAlchemy(SQLAlchemy):
    Column: Callable
    String: Callable
    Integer: Callable
    Float: Callable
    DateTime: DateTime
    relationship: Callable
    ForeignKey: Callable
    Enum: Callable
    Text: Callable
    Sequence: Callable
    Boolean: Callable


db = SQLAlchemy()
migrate = Migrate(compare_type=True)
marsh = Marshmallow()

basestring = (str, bytes)
Column = db.Column
relationship = db.relationship
ForeignKey = db.ForeignKey
Sequence = db.Sequence


class BaseEnum(Enum):

    @classmethod
    def choices_dict_desc(cls):
        return {key.name: key.value.replace('_', ' ') for key in cls}

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    @classmethod
    def all(cls):
        return [key.value for key in cls]


def initialize_db(app):
    db.init_app(app)
    migrate.init_app(app, db)
    marsh.init_app(app)
    return app

# ------- Override Class, function, var for Database SQL
# from flask-cookiecutter
"""Database module, including the SQLAlchemy database object and DB-related utilities."""


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

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
        return self

    def delete(self, commit: bool = True) -> None:
        """Remove the record from the database."""
        try:
            db.session.delete(self)
            if commit:
                return db.session.commit()
        except:
            db.session.rollback()
        return


class Model(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""

    __abstract__ = True

    # exceptions like django :)
    DoesNotExist = exc.NoResultFound
    MultipleObjectsReturned = exc.MultipleResultsFound

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self}>"

    def __str__(self):
        return str(self.id)


class PkModel(Model):
    """Base model class that includes CRUD convenience methods, plus adds a 'primary key' column named ``id``."""

    __abstract__ = True
    id = Column(db.Integer, primary_key=True, autoincrement=True)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        if any(
            (
                isinstance(record_id, basestring) and record_id.isdigit(),
                isinstance(record_id, (int, float)),
            )
        ):
            return cls.query.get(int(record_id))
        return None


def reference_col(tablename, nullable=False, pk_name="id", foreign_key_kwargs=None, column_kwargs=None):
    """Column that adds primary key foreign key reference.

    Usage: ::

        category_id = reference_col('category')
        category = relationship('Category', backref='categories')
    """
    foreign_key_kwargs = foreign_key_kwargs or {}
    column_kwargs = column_kwargs or {}

    return Column(
        db.ForeignKey(f"{tablename}.{pk_name}", **foreign_key_kwargs),
        nullable=nullable,
        **column_kwargs,
    )
