#!/usr/bin/python3
"""Module for BaseModel"""

import uuid
from datetime import datetime

import models


class BaseModel:
    """Class for BaseModel"""

    def __init__(self, *args, **kwargs):
        """BaseModel Instance Initializer

         Args:
            - *args: list of arguments
            - **kwargs: dict of key-values arguments
        """
        if kwargs is not None and kwargs != {}:
            for key in kwargs:
                if key == "created_at":
                    self.__dict__["created_at"] = datetime.strptime(
                        kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
                elif key == "updated_at":
                    self.__dict__["updated_at"] = datetime.strptime(
                        kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    self.__dict__[key] = kwargs[key]
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
