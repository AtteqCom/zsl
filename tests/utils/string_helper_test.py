from unittest.case import TestCase

from zsl.utils.string_helper import camelcase_to_underscore, join_list, underscore_to_camelcase


class InflectionTestCase(TestCase):
    def testCamelCaseToUnderscore(self):
        self.assertEquals(
            "camel_case_to_underscore",
            camelcase_to_underscore("camelCaseToUnderscore"),
            "CC to usc conversion"
        )
        self.assertEquals(
            "camel_case_to_underscore",
            camelcase_to_underscore("CamelCaseToUnderscore"),
            "CC to usc conversion"
        )

    def testUnderscoreToCamelCase(self):
        self.assertEquals(
            "camelCaseToUnderscore",
            underscore_to_camelcase("camel_case_to_underscore", False),
            "CC to usc conversion"
        )
        self.assertEquals(
            "CamelCaseToUnderscore",
            underscore_to_camelcase("camel_case_to_underscore"),
            "CC to usc conversion"
        )
        self.assertEquals(
            "CamelCaseToUnderscore",
            underscore_to_camelcase("camel_case_to_underscore", True),
            "CC to usc conversion"
        )


class JoinListTestCase(TestCase):
    def testJoin(self):
        self.assertEqual('A, B', join_list(['a', 'b'], transform=lambda x: x.upper()))

    def testIdentity(self):
        self.assertEqual('a, b', join_list('a, b'))

    def testNone(self):
        self.assertEqual(None, join_list(None))
