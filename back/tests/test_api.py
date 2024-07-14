from fastapi.testclient import TestClient
from unittest import TestCase

from src.api.app import get_app
from src.api.search.engine import get_search_engine

from mocked import get_mocked_search_engine

app = get_app()
client = TestClient(app)

app.dependency_overrides[get_search_engine] = get_mocked_search_engine


class FastAPITest(TestCase):

    terms = [
        "direito do consumidor",
        "direito do trabalhador",
        "direito das mulheres",
    ]

    def test_health(self):
        """
        Test if server is alive.
        """
        response = client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_create_term(self):
        """
        Test creating terms.
        """
        # There should be nothing in the search engine.
        search_engine = get_mocked_search_engine()
        self.assertListEqual(search_engine.get_all_terms(), list())

        # Create terms.
        headers = {
            "Content-Type": "application/json",
        }

        for term in self.terms:
            mutation = f'mutation {{createTerm(term: "{term}")}}'

            response = client.post("graphql/", json={"query": mutation}, headers=headers)
            self.assertEqual(response.status_code, 200)

        # Check if the terms were created successfully.
        search_engine = get_mocked_search_engine()
        self.assertListEqual(search_engine.get_all_terms(), self.terms)

    def test_get_all_terms(self):
        """
        Test getting all terms from the search engine.
        """
        headers = {
            "Content-Type": "application/json",
        }

        response = client.post("graphql/", json={"query": "query {allTerms}"}, headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["allTerms"], self.terms)

    def test_search_terms(self):
        """
        Test searching for terms.
        """
        test_cases = [
            {"searchInput": "direito", "expected": self.terms},
            {
                "searchInput": "direito do con",
                "expected": [
                    "direito do consumidor",
                ],
            },
            {
                "searchInput": "direito do tra",
                "expected": [
                    "direito do trabalhador",
                ],
            },
            {
                "searchInput": "direito da",
                "expected": [
                    "direito das mulheres",
                ],
            },
        ]

        headers = {
            "Content-Type": "application/json",
        }

        for test_case in test_cases:
            text = test_case["searchInput"]

            query = f'query {{searchTerms(text: "{text}")}}'
            response = client.post("graphql/", json={"query": query}, headers=headers)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["data"]["searchTerms"], test_case["expected"])
