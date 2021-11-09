#!/usr/bin/python3
"""Entry point of the command interpreter"""
import cmd


class HBNBCommand(cmd.Cmd):
    """Class for the command interpreter"""

    prompt = "(hbnb) "

    def do_EOF(self, line):
        """Handles end of file character"""
        print()
        return True

    def do_quit(self, line):
        """Quits the program"""
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
