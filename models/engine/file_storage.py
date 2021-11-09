#!/usr/bin/python3
"""FileStorage that serializes instances to
JSON file and deserializes JSON file to instances"""
import json


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
                file_object = {k: self.classes()[v["__class__"]](**v)
                               for k, v in file_object.items()
                               }
                FileStorage.__objects = file_object
        except FileNotFoundError:
            pass
