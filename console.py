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
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }

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

    def do_update(self, args):
        """ Updates a certain object with new info """
        c_name = c_id = att_name = att_val = kwargs = ''

        # isolate cls from id/args, ex: (<cls>, delim, <id/args>)
        args = args.partition(" ")
        if args[0]:
            c_name = args[0]
        else:  # class name not present
            print("** class name missing **")
            return
        if c_name not in self.class_list:  # class name invalid
            print("** class doesn't exist **")
            return

        # isolate id from args
        args = args[2].partition(" ")
        if args[0]:
            c_id = args[0]
        else:  # id not present
            print("** instance id missing **")
            return

        # generate key from class and id
        key = c_name + "." + c_id

        # determine if key is present
        if key not in storage.all():
            print("** no instance found **")
            return

        # first determine if kwargs or args
        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []  # reformat kwargs into list, ex: [<name>, <value>, ...]
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else:  # isolate args
            args = args[2]
            if args and args[0] == '\"':  # check for quoted arg
                second_quote = args.find('\"', 1)
                att_name = args[1:second_quote]
                args = args[second_quote + 1:]

            args = args.partition(' ')

            # if att_name was not quoted arg
            if not att_name and args[0] != ' ':
                att_name = args[0]
            # check for quoted val arg
            if args[2] and args[2][0] == '\"':
                att_val = args[2][1:args[2].find('\"', 1)]

            # if att_val was not quoted arg
            if not att_val and args[2]:
                att_val = args[2].partition(' ')[0]

            args = [att_name, att_val]

        # retrieve dictionary of current objects
        new_dict = storage.all()[key]

        # iterate through attr names and values
        for i, att_name in enumerate(args):
            # block only runs on even iterations
            if (i % 2 == 0):
                att_val = args[i + 1]  # following item is value
                if not att_name:  # check for att_name
                    print("** attribute name missing **")
                    return
                if not att_val:  # check for att_value
                    print("** value missing **")
                    return
                # type cast as necessary
                if att_name in self.types:
                    att_val = self.types[att_name](att_val)

                # update dictionary with name, value pair
                new_dict.__dict__.update({att_name: att_val})

        new_dict.save()  # save updates to file

    def __count(self, line):
        """ Retrieve the number of instances of a class """
        count = 0
        for key, value in storage.all().items():
            if value.__class__.__name__ == line:
                count += 1
        print(count)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
