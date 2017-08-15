"""
:mod:`zsl.utils.command_dispatcher`
-----------------------------------

.. moduleauthor:: peter morihladko
"""
from __future__ import unicode_literals

from builtins import object
import inspect


class CommandDispatcher(object):
    """
    A simple class for command dictionary. A command is a function
    which can take named parameters.
    """

    def __init__(self):
        """
        Create command dictionary
        """

        self.commands = {}

    def command(self, fn):
        """
        Add method or function to dispatcher. Can be use as a nice
        decorator.

        :param fn: function or method
        :type fn: function
        :return: the same function
        :rtype: function
        """
        self.commands[fn.__name__] = fn

        return fn

    """alias for ``CommandDispatcher.command``"""
    add_function = command

    def execute_command(self, command, args=None):
        """
        Execute a command

        :param command: name of the command
        :type command: str
        :param args: optional named arguments for command
        :type args: dict
        :return: the result of command
        :raises KeyError: if command is not found
        """

        if args is None:
            args = {}

        command_fn = self.commands[command]

        return command_fn(**args)

    def bound(self, instance):
        """
        Return a new dispatcher, which will switch all command functions
        with bounded methods of given instance matched by name. It will
        match only regular methods.

        :param instance: object instance
        :type instance: object
        :return: new Dispatcher
        :rtype: CommandDispatcher
        """

        bounded_dispatcher = CommandDispatcher()
        bounded_dispatcher.commands = self.commands.copy()

        for name in self.commands:
            method = getattr(instance, name, None)

            if method and inspect.ismethod(method) and method.__self__ == instance:
                bounded_dispatcher.commands[name] = method

        return bounded_dispatcher
