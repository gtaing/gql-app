import unittest as unittest
from graphene.test import Client
from app.gql.query import schema


class TestQuery(unittest.TestCase):

    def test_job_query(self):

        client = Client(schema)

        result = client.execute(
            """
        query {
          jobs {
            id
            title
            description
            employerId
          }
        }
        """
        )

        print(result)
        self.assertIsNotNone(result)
