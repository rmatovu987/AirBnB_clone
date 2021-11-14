#!/usr/bin/python3
"""Entry point of the command interpreter"""
import cmd
import json
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

    def default(self, line):
        """ Method used to “intercept” STDOUT"""
        methods = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.__count,
            "update": self.do_update
            }
        i = line.split(".")
        _class = i[0]
        i_finder = i[1].split("(")
        method = i_finder[0]
        attr = i_finder[1].replace(')', "").replace('"', "")
        id_finder = attr.split(", ")
        idclass_ = id_finder[0]
        if _class in self.class_list and method in methods:
            if method == "all" or method == "count":
                methods[method](_class)
            elif method == "update":
                attr = attr.split(", ")
                attr_name = attr[1]
                attr_value = attr[2]
                methods[method]("{} {} {} {}".format(_class,
                                idclass_, attr_name, attr_value))
            else:
                methods[method]("{} {}".format(_class, idclass_))
        else:
            cmd.Cmd.default(self, line)

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

    def do_update(self, arg):
        """Update an instance based on class name"""
        args_list = shlex.split(arg)
        new_dict = storage.all()  # This is a dict of instances.
        # list[0] = classname
        # list[1] = id
        # list[2] = attribute name
        # list[3] = "atribute value"
        if len(args_list) < 1:
            print("** class name missing **")
        # Check if the class name doesn’t exist
        elif args_list[0] not in self.class_list:
            print("** class doesn't exist **")
        # Check if the id is given as a parameter
        elif len(args_list) < 2:
            print("** instance id missing **")
        else:
            new_key = args_list[0] + '.' + args_list[1]  # This is the key
            if new_key not in new_dict.keys():
                print("** no instance found **")
            elif len(args_list) < 3:
                print("** attribute name missing **")
            elif len(args_list) < 4:
                print("** value missing **")
            else:
                # Get the instance
                instance = new_dict[new_key]
                # Get the attribute to update from that instance
                try:
                    # Get the type of the attribute
                    # Cast the attribute value to corresponding type
                    up_attr = getattr(instance, args_list[2])
                    attr_type = type(up_attr)
                    casted_val = eval('attr_type' + '(' + args_list[3] + ')')
                    setattr(instance, args_list[2], casted_val)
                except Exception:
                    # If attribute does not exist, save value to set.
                    setattr(instance, args_list[2], args_list[3])
                # Set attribute with new value
                # Save changes to JSON file
                storage.save()

    def __count(self, line):
        """ Retrieve the number of instances of a class """
        count = 0
        for key, value in storage.all().items():
            if value.__class__.__name__ == line:
                count += 1
        print(count)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
