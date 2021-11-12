#!/usr/bin/python3
"""Entry point of the command interpreter"""
import cmd
import shlex

from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class HBNBCommand(cmd.Cmd):
    """Class for the command interpreter"""

    class_list = ["BaseModel", "User", "Amenity", "City",
                  "Place", "Review", "State"]
    prompt = "(hbnb) "

    @staticmethod
    def do_EOF(line):
        """Handles end of file character"""
        print()
        return True

    @staticmethod
    def do_quit(line):
        """Quits the program"""
        return True

    def emptyline(self):
        """Execute nothing"""
        pass

    def do_create(self, line):
        """Creates a new instance of BaseModel, saves it
        (to the JSON file) and prints the id. Ex: $ create BaseModel"""
        if not line:
            print("** class name missing **")
        elif line not in self.class_list:
            print("** class doesn't exist **")
        else:
            b = eval(line)()
            b.save()
            print(b.id)

    def do_show(self, line):
        """Prints string instance based on class name"""
        i = line.split()
        if not line:
            print("** class name missing **")
            return
        elif i[0] not in self.class_list:
            print("** class doesn't exist **")
            return
        elif len(i) == 1:
            print("** instance id missing **")
            return
        data = storage.all()
        key = i[0] + "." + i[1]
        if key not in data.keys():
            print("** no instance found **")
        else:
            print(data[key])

    def do_destroy(self, line):
        """Delete an instance based on class name"""
        i = line.split()
        if not line:
            print("** class name missing **")
            return
        elif i[0] not in self.class_list:
            print("** class doesn't exist **")
            return
        elif len(i) == 1:
            print("** instance id missing **")
            return
        data = storage.all()
        key = i[0] + "." + i[1]
        if key not in data.keys():
            print("** no instance found **")
        else:
            del storage.all()[key]
            storage.save()
            return

    def do_all(self, line):
        """Prints all string representation of all instances based on
        class name"""
        i = line.split()
        list_obj = []
        data = storage.all()
        if not line:
            for value in data.values():
                list_obj.append(value.__str__())
            print(list_obj)
        elif i[0] not in self.class_list:
            print("** class doesn't exist **")
        else:
            for key, value in data.items():
                if i[0] in key:
                    list_obj.append(data[key].__str__())
            print(list_obj)

    def do_update(self, line):
        """Update an instance based on class name"""
        i = shlex.split(line)
        if not line:
            print("** class name missing **")
            return
        elif i[0] not in self.class_list:
            print("** class doesn't exist **")
            return
        elif len(i) == 1:
            print("** instance id missing **")
            return
        data = storage.all()
        key = i[0] + "." + i[1]
        if key not in data:
            print("** no instance found **")
        elif len(i) == 2:
            print("** attribute name missing **")
        elif len(i) == 3:
            print("** value missing **")
        else:
            setattr(data[key], i[2], i[3])
            storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
