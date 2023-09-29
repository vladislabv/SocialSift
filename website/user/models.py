# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt
from flask_login import UserMixin
# import types
from mongoengine import StringField, DateTimeField, BooleanField, ReferenceField
from mongoengine.queryset import CASCADE

from website.database import PkDocument

from werkzeug.security import check_password_hash, generate_password_hash


class MongoUserMixin(UserMixin):
    """Custom user mixin for mongoengine models."""
    
    @property
    def password(self):
        """Hashed password."""
        return self._password

    @password.setter
    def password(self, value):
        """Set password."""
        self._password = generate_password_hash(value)
        
    def check_password(self, value):
        """Check password."""
        return check_password_hash(self._password, value)


class User(MongoUserMixin, PkDocument):
    """A user of the app."""
    username = StringField(max_length=80, unique=True, required=True)
    email = StringField(max_length=80, unique=True, required=True)
    password = StringField(required=True)
    created_at = DateTimeField(required=True, default=dt.datetime.utcnow)
    first_name = StringField(max_length=30)
    last_name = StringField(max_length=30)
    active = BooleanField(default=False)
    is_admin = BooleanField(default=False)

    @property
    def full_name(self):
        """Full user name."""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<User({self.username})>"
    
    def save(self, *args, **kwargs):
        """Override save method to hash the password before saving."""
        if 'password' in self._data:  # Check if the password was provided
            self._data['password'] = generate_password_hash(self._data['password'])  # Hash the password
        super(User, self).save(*args, **kwargs)  # Save the document

    def set_password(self, password):
        """Set the password by hashing it."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check if the given password matches the hashed password."""
        return check_password_hash(self.password, password)


class Role(PkDocument):
    """A role for a user."""
    name = StringField(max_length=80, unique=True, required=True)
    user = ReferenceField(User, reverse_delete_rule=CASCADE)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Role({self.name})>"