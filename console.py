#!/usr/bin/python3
"""
entry point of the command interpreter
"""
import cmd
import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import shlex
import re


class HBNBCommand(cmd.Cmd):
    """defines the cmd class"""
    prompt = "(hbnb) "
    our_classes = ['BaseModel', 'User', 'State',
                   'City', 'Amenity', 'Place', 'Review']

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, line):
        """EOF command to exit the program"""
        return True

    def emptyline(self):
        """when an empty line is entered, it should not execute anything"""
        pass

    def do_create(self, line):
        """
        Creates a new instance of BaseModel
        saves it (to the JSON file) and prints the id
        Ex: $ create BaseModel
        """
        command = self.parseline(line)[0]

        if command is None:
            print("** class name missing **")
        elif command not in self.our_classes:
            print("** class doesn't exist **")
        else:
            new_obj = eval(command)()
            new_obj.save()
            print(new_obj.id)

    def do_show(self, line):
        """
        Prints the string representation of an instance
        based on the class name and id
        Ex: $ show BaseModel 1234-1234-1234
        """
        command = self.parseline(line)[0]
        arg = self.parseline(line)[1]

        if command is None:
            print("** class name missing **")
        elif command not in self.our_classes:
            print("** class doesn't exist **")
        elif arg == "":
            print("** instance id missing **")
        else:
            key = command + "." + arg
            inst_class_id = models.storage.all().get(key)
            if inst_class_id is None:
                print("** no instance found **")
            else:
                print(inst_class_id)

    def do_destroy(self, line):
        """
        Deletes an instance based on the class name and id
        (save the change into the JSON file).
        Ex: $ destroy BaseModel 1234-1234-1234
        """
        command = self.parseline(line)[0]
        arg = self.parseline(line)[1]

        if command is None:
            print("** class name missing **")
        elif command not in self.our_classes:
            print("** class doesn't exist **")
        elif arg == "":
            print("** instance id missing **")
        else:
            key = command + "." + arg
            inst_class_id = models.storage.all().get(key)
            if inst_class_id is None:
                print("** no instance found **")
            else:
                del models.storage.all()[key]
                models.storage.save()

    def do_all(self, line):
        """
        Prints all string representation of all instances
        based or not on the class name.
        Ex: $ all BaseModel or $ all
        """
        command = self.parseline(line)[0]
        objs = models.storage.all()

        if command is None:
            print([str(objs[obj]) for obj in objs])
        elif command in self.our_classes:
            keys = objs.keys()
            print([str(objs[key]) for key in keys if key.startswith(command)])
        else:
            print("** class doesn't exist **")

    def do_update(self, line):
        """
        Updates an instance based on the class name and id
        by adding or updating attribute (save the change into the JSON file).
        Ex: $ update BaseModel 1234-1234-1234 email "aibnb@mail.com"
        """
        args = shlex.split(line)
        args_size = len(args)

        if args_size == 0:
            print("** class name missing **")
        elif args[0] not in self.our_classes:
            print("** class doesn't exist **")
        elif args_size == 1:
            print("** instance id missing **")
        else:
            key = args[0] + "." + args[1]
            inst_class_id = models.storage.all().get(key)
            if inst_class_id is None:
                print("** no instance found **")
            elif args_size == 2:
                print("** attribute name missing **")
            elif args_size == 3:
                print("** value missing **")
            else:
                setattr(inst_class_id, args[2], args[3])
                models.storage.save()

    @classmethod
    def get_instances(self, instance=""):
        """
        gets the elements created by the console
        obtains the information of all the instances
        created in the file `file.json` that is used as the storage engine.
        """
        objs = models.storage.all()

        if instance:
            keys = objs.keys()
            return [str(value) for key, value in objs.items()
                    if key.startswith(instance)]

        return [str(value) for key, value in objs.items()]

    def default(self, line):
        """
        When the command prefix is not recognized, this method
        looks for whether the command entered has the syntax:
            "<class name>.<method name>" or not,
        and links it to the corresponding method in case the
        class exists and the method belongs to the class.
        """
        if '.' in line:
            splitted = re.split(r'\.|\(|\, |\, |\)', line)
            class_name = splitted[0]
            method_name = splitted[1]

            if class_name in self.our_classes:
                if method_name == 'all':
                    print(self.get_instances(class_name))
                elif method_name == 'count':
                    print(len(self.get_instances(class_name)))
                elif method_name == 'show':
                    class_id = splitted[2][1:-1]
                    self.do_show(class_name + ' ' + class_id)
                elif method_name == 'destroy':
                    class_id = splitted[2][1:-1]
                    self.do_destroy(class_name + ' ' + class_id)
                elif method_name == 'update':
                        class_id = splitted[2][1:-1]
                        attr_name = splitted[3][1:-1]
                        attr_value = splitted[4][1:-1]
                        self.do_update(class_name + ' ' + class_id + ' ' + attr_name + ' ' + attr_value)

        """work in progress if '{}' in line:
            if class_name in self.our_classes:
                if method_name == 'update':
                    # splitted = re.split(r'\.|\(|\, {|\: |\, |\: |\})', line)
                    # /D*+
                    # splitted = re.split(r'\.|\(|\, |\)', line)
                    #class_name = splitted[0]
                    #method_name = splitted[1]
                    #class_id = splitted[2][1:-1]
                    #class_dict = splitted[3] = {}
                    #for key, value in class_dict:
                    #attr_name1 = splitted[3][1:-1]
                    #attr_value1 = splitted[4][1:-1]
                    #attr_name2 = splitted[5][1:-1]
                    #attr_value2 = splitted[6][1:-1]
                    self.do_update(class_name + ' ' + class_id + ' ' + attr_name1 + ' ' + attr_value1 + ' ' + attr_name2 + ' ' + attr_value2)"""


if __name__ == '__main__':
    HBNBCommand().cmdloop()
