from unittest.case import TestCase

from sqlalchemy.orm import Session

from tests.resource.resource_test_helper import UserModel, create_resource_test_data
from zsl import Zsl
from zsl.resource.resource_helper import filter_from_url_arg
from zsl.testing.db import IN_MEMORY_DB_SETTINGS


class ModelResourceTest(TestCase):

    def setUp(self):
        Zsl(__name__, config_object=IN_MEMORY_DB_SETTINGS)
        create_resource_test_data()

    def testFilterEmpty(self):
        query = Session().query(UserModel)
        query = filter_from_url_arg(UserModel, query, "")

        contains_where_clause = 'where' in str(query).lower()

        self.assertFalse(contains_where_clause, "The query should not contain any filter")

    def testFilterMultipleArgs(self):
        query = Session().query(UserModel)
        filter_by = 'id==1,id==2,id==5'

        query = filter_from_url_arg(UserModel, query, filter_by)

        # the where clause should be: 'id == 1 or id == 2 or id == 5'
        where_clause = str(query).lower().split('where')[1]
        filter_clauses = where_clause.split('or')

        self.assertEqual(len(filter_clauses), 3, "There should be 3 filter clauses separated by OR")

    def testFilterCombinationsOfArgs(self):
        query = Session().query(UserModel)
        filter_by = 'id==1,id==2,name==julius,id==5'

        query = filter_from_url_arg(UserModel, query, filter_by)
        print(str(query))

        # the where clause should be: '(id == 1 or id == 2 or id == 5) and name == julius'
        where_clause = str(query).lower().split('where')[1]
        filter_conjunctions = where_clause.split('and')
        self.assertEqual(len(filter_conjunctions), 2, "There should be conjunction of two clauses in the query")

        first_clause = filter_conjunctions[0].split('or')
        second_clause = filter_conjunctions[1].split('or')

        self.assertTrue(len(first_clause) == 3 or len(second_clause) == 3,
                        "One of the clauses should have 3 conditions")
        self.assertTrue(len(first_clause) == 1 or len(second_clause) == 1, "One of the clauses should have 1 condition")
