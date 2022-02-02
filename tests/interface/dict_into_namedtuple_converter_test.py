from decimal import Decimal
from typing import NamedTuple, Optional, Union
from unittest import TestCase

from zsl.interface.dict_into_namedtuple_converter import DictIntoNamedTupleConverter, ModelConversionError


class DictIntoNamedTupleConverterTest(TestCase):

    def setUp(self) -> None:
        self.converter = DictIntoNamedTupleConverter()

    def test_correctly_converts_simple_types(self):
        class Model(NamedTuple):
            text: str
            number: int
            floating_number: float
            logic_value: bool

        result = self.converter.convert({
            'text': "We're all stories, in the end. Just make it a good one, eh?",
            'number': 11,
            'floating_number': 5.13,
            'logic_value': True
        }, Model)

        self.assertIsInstance(result.text, str, 'Incorrectly parsed str type')
        self.assertEqual(
            result.text, "We're all stories, in the end. Just make it a good one, eh?", 'Incorrectly parsed str value'
        )

        self.assertIsInstance(result.number, int, 'Incorrectly parsed int type')
        self.assertEqual(result.number, 11, 'Incorrectly parsed int value')

        self.assertIsInstance(result.floating_number, float, 'Incorrectly parsed float type')
        self.assertEqual(result.floating_number, 5.13, 'Incorrectly parsed float value')

        self.assertIsInstance(result.logic_value, bool, 'Incorrectly parsed bool type')
        self.assertTrue(result.logic_value, 'Incorrectly parsed bool value')

    def test_correctly_converts_decimal_type(self):
        class Model(NamedTuple):
            float: Decimal
            int: Decimal
            decimal: Decimal

        result = self.converter.convert({
            'float': 35.26,
            'int': 10,
            'decimal': Decimal(12.42)
        }, Model)

        self.assertIsInstance(result.float, Decimal, 'Incorrectly parsed float as decimal type')
        self.assertEqual(result.float, Decimal(35.26), 'Incorrectly parsed float to decimal value')

        self.assertIsInstance(result.int, Decimal, 'Incorrectly parsed int as decimal type')
        self.assertEqual(result.int, Decimal(10), 'Incorrectly parsed int to decimal value')

        self.assertIsInstance(result.decimal, Decimal, 'Incorrectly parsed decimal type')
        self.assertEqual(result.decimal, Decimal(12.42), 'Incorrectly parsed decimal value')

    def test_correctly_converts_optional_type__when_value_missing(self):
        class Model(NamedTuple):
            val: Optional[str]

        result = self.converter.convert({}, Model)

        self.assertIsNone(result.val, 'Incorrectly parsed missing optional value')

    def test_correctly_converts_optional_type__when_value_not_missing(self):
        class Model(NamedTuple):
            val: Optional[str]

        result = self.converter.convert({
            'val': "Good men don't need rules. Today is not the day to find out why I have so many."
        }, Model)

        self.assertIsInstance(result.val, str, 'Incorrectly parsed optional str type')
        self.assertEqual(
            result.val,
            "Good men don't need rules. Today is not the day to find out why I have so many.",
            'Incorrectly parsed optional str value'
        )

    def test_correctly_converts_union_type__when_first_type(self):
        class Model(NamedTuple):
            val: Union[int, float, str]

        result = self.converter.convert({
            'val': 42
        }, Model)

        self.assertIsInstance(result.val, int, 'Incorrectly parsed int in union type')
        self.assertEqual(result.val, 42, 'Incorrectly parsed int in union value')

    def test_correctly_converts_union_type__when_last_type(self):
        class Model(NamedTuple):
            val: Union[int, float, str]

        result = self.converter.convert({
            'val': '542'
        }, Model)

        self.assertIsInstance(result.val, str, 'Incorrectly parsed str in union type')
        self.assertEqual(result.val, '542', 'Incorrectly parsed str in union value')

    def test_correctly_converts_optional_union__when_value_is_missing(self):
        class Model(NamedTuple):
            val: Optional[Union[str, int]]

        result = self.converter.convert({}, Model)

        self.assertIsNone(result.val, 'Incorrectly parsed missing optional value')

    def test_correctly_converts_optional_union__when_value_is_not_missing(self):
        class Model(NamedTuple):
            val: Optional[Union[str, int]]

        result = self.converter.convert({
            'val': 5465132
        }, Model)

        self.assertIsInstance(result.val, int, 'Incorrectly parsed int in optional union type')
        self.assertEqual(result.val, 5465132, 'Incorrectly parsed int in optional union value')

    def test_correctly_converts_with_default_value__when_default_not_used(self):
        class Model(NamedTuple):
            val: str = "Don't blink. Blink and you're dead. They are fast. Faster than you can believe."

        result = self.converter.convert({
            'val': 'Doctor Who?'
        }, Model)

        self.assertIsInstance(result.val, str, 'Incorrectly parsed str type with default value')
        self.assertEqual(result.val, 'Doctor Who?', 'Incorrectly parsed str type with default value')

    def test_correctly_converts_with_default_value__when_default_should_be_used(self):
        class Model(NamedTuple):
            val: str = "Don't blink. Blink and you're dead. They are fast. Faster than you can believe."

        result = self.converter.convert({}, Model)

        self.assertIsInstance(result.val, str, 'Incorrectly parsed str type with default value')
        self.assertEqual(
            result.val,
            "Don't blink. Blink and you're dead. They are fast. Faster than you can believe.",
            'Incorrectly parsed str type with default value'
        )

    def test_error_when_model_is_not_namedtuple(self):
        class Model:
            val: str

        with self.assertRaises(Exception):
            self.converter.convert({}, Model)

    def test_error_when_non_optional_field_missing_in_request(self):
        class Model(NamedTuple):
            val: str

        with self.assertRaises(ModelConversionError):
            self.converter.convert({}, Model)

    def test_error_when_field_in_request_not_in_model(self):
        class Model(NamedTuple):
            val: str

        with self.assertRaises(ModelConversionError):
            self.converter.convert({'text': "One may tolerate a world of demons for the sake of an angel."}, Model)

    def test_error_when_simple_type_mismatch(self):
        class Model(NamedTuple):
            text: str

        with self.assertRaises(ModelConversionError):
            self.converter.convert({'text': 84521}, Model)

    def test_error_when_union_type_mismatch(self):
        class Model(NamedTuple):
            val: Union[str, int]

        with self.assertRaises(ModelConversionError):
            self.converter.convert({'val': 3.25}, Model)

    def test_error_when_optional_type_mismatch(self):
        class Model(NamedTuple):
            val: Optional[str]

        with self.assertRaises(ModelConversionError):
            self.converter.convert({'val': 3.65}, Model)
