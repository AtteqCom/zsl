__author__ = 'julius'

from unittest.case import TestCase

from werkzeug.datastructures import ImmutableMultiDict

from zsl.utils.request_helper import args_to_dict


class InflectionTestCase(TestCase):

    def test_empty(self):
        args = ImmutableMultiDict([])
        args_dict = args_to_dict(args)
        self.assertEqual(args_dict, {}, "Arguments dictionary should be empty for empty arguments object")

    def test_one_param(self):
        args = ImmutableMultiDict([('a', 1)])
        args_dict = args_to_dict(args)
        self.assertEqual(args_dict, {'a': 1}, "Arguments dictionary should contain the one argument")

    def test_more_params(self):
        args = ImmutableMultiDict([('a', 1), ('b', 2), ('c', 42)])
        args_dict = args_to_dict(args)
        self.assertEqual(args_dict, {'a': 1, 'b': 2, 'c': 42}, "Arguments dictionary should contain the same "
                                                               "parameters as the arguments object")

    def test_multi_param(self):
        args = ImmutableMultiDict([('a', 2), ('a', 4), ('a', 8)])
        args_dict = args_to_dict(args)
        self.assertEqual(args_dict, {'a': [2, 4, 8]}, "The param should be list of all of its values")

    def test_multi_params_with_other_params(self):
        args = ImmutableMultiDict([('a', 3), ('b', 'PWR UP'), ('a', 9), ('a', 27)])
        args_dict = args_to_dict(args)
        self.assertEqual(args_dict, {'a': [3, 9, 27], 'b': 'PWR UP'}, "Arguments dictionary should contain the same "
                                                                      "parameters as the arguments object")
