import types
import unittest

from zsl.utils.command_dispatcher import CommandDispatcher

__author__ = 'peter'


class TestCommandDispatcher(unittest.TestCase):
    def setUp(self):
        self.dispatcher = CommandDispatcher()

    def test_add_function(self):

        def dummy_function():
            pass

        self.assertEqual(len(self.dispatcher.commands), 0, "Empty commands")

        self.dispatcher.add_function(dummy_function)

        self.assertEqual(len(self.dispatcher.commands), 1, "Command added")
        self.assertEqual(self.dispatcher.commands[dummy_function.__name__],
                         dummy_function,
                         "Command added")

    def test_command_decorator(self):

        def another_dummy_fn():
            pass

        decorated_fn = self.dispatcher.command(another_dummy_fn)

        self.assertEqual(decorated_fn,
                         another_dummy_fn,
                         "Decorator hasn't returned the same function")

        @self.dispatcher.command
        def dummy_function():
            pass

        self.assertEqual(self.dispatcher.commands[dummy_function.__name__],
                         dummy_function,
                         "Decorator didn't decorate")

    def test_command_execute(self):
        dispatcher = self.dispatcher

        @dispatcher.command
        def return_five():
            return 5

        @dispatcher.command
        def adder(a, b):
            return a + b

        @dispatcher.command
        def summer(n, **kwargs):
            return sum(map(lambda x: x*n, kwargs.values()))

        self.assertEqual(dispatcher.execute_command('return_five'),
                         5, "Command didn't execute properly")

        self.assertEqual(dispatcher.execute_command('adder', {'a': 1, 'b': 2}),
                         adder(1, 2),
                         "Command has not taken given arguments")

        # testparameters
        self.assertRaises(TypeError,
                          dispatcher.execute_command, 'adder', {'a': 1, 'b': 2, 'e': 3})
        self.assertRaises(TypeError, dispatcher.execute_command, 'adder')

        self.assertEquals(dispatcher.execute_command('summer', {'n': 2, '1': 1, '2': 2, '3': 3}),
                          sum([2, 4, 6]),
                          "Command doesn't support kwarg parameters")

        with self.assertRaises(KeyError):
            dispatcher.execute_command('error_command')

    def test_bound(self):
        dispatcher = self.dispatcher

        class C(object):
            def __init__(self, a, b):
                self._a = a
                self._b = b

            @dispatcher.command
            def get_sum(self, x, y):
                return self._a + self._b + x + y

        class D(object):
            def __init__(self, a, b):
                self._a = a
                self._b = b

            @dispatcher.command
            def get_other_sum(self, x, y):
                return self._a + self._b + x + y

        @dispatcher.command
        def dummy_fun():
            return 5

        c = C(1, 2)
        d = D(10, 20)

        bounded_dispatcher = dispatcher.bound(c)

        self.assertEqual(bounded_dispatcher.commands['get_sum'], c.get_sum,
                         "Bound has not bounded the method")
        self.assertEqual(bounded_dispatcher.execute_command('get_sum', {'x': 10, 'y': 200}),
                         c.get_sum(10, 200),
                         "Bound method has false result")

        self.assertIs(type(bounded_dispatcher.commands['get_other_sum']), types.FunctionType,
                      "Bound has bounded a foreign method")
        self.assertEqual(bounded_dispatcher.execute_command('get_other_sum', {'self': d, 'x': 1000, 'y': 300}),
                         d.get_other_sum(1000, 300),
                         "Bound has returned a false result for not bounded method")

        self.assertEqual(bounded_dispatcher.execute_command('dummy_fun'),
                         5, "Bound has returned a false result for normal function")
