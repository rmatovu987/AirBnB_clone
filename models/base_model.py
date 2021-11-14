#!/usr/bin/python3
"""Module for BaseModel"""

import uuid
from datetime import datetime

import models


class BaseModel:
    """Class for BaseModel"""
    def __init__(self, *args, **kwargs):
        """BaseModel Instance Initializer"""
        if kwargs:
            for key, value in kwargs.items():
                if key in ["created_at", "updated_at"]:
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key not in ["__class__"]:
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """Return a human readable string"""
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        """Updates instance of updated_at with current datetime"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary containing all the key/values of
        the __dict__ instance"""
        dic = dict(self.__dict__)
        dic["__class__"] = self.__class__.__name__
        dic["created_at"] = self.created_at.isoformat()
        dic["updated_at"] = self.updated_at.isoformat()
        return dic
