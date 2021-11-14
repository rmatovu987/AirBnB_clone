#!/usr/bin/python3
"""FileStorage that serializes instances to
JSON file and deserializes JSON file to instances"""

import json

from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    """Class for FileStorage"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj"""
        key = obj.__class__.__name__ + "." + str(obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes the __objects to JSON file"""
        dict1 = {}
        for key, value in FileStorage.__objects.items():
            dict1[key] = value.to_dict()

        with open(FileStorage.__file_path, "w") as save_file:
            json.dump(dict1, save_file)

    def reload(self):
        """Deserializes the JSON file to __objects
        only if the JSON file exists"""
        try:
            with open(FileStorage.__file_path, "r") as file:
                file_object = json.load(file)
                for key, value in file_object.items():
                    object1 = eval(value["__class__"])(**value)
                    FileStorage.__objects[key] = object1
        except FileNotFoundError:
            pass
