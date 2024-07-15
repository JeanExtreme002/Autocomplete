from unittest import IsolatedAsyncioTestCase
import time
import requests

from src.api.search.engine import SearchEngine, get_search_engine


def clear_search_engine(search_engine) -> None:
    """
    Delete all documents from the search engine.
    """
    index_url = f"{search_engine.base_url}/{search_engine.term_index_name}"

    query = {"query": {"match_all": {}}}
    response = requests.post(f"{index_url}/_delete_by_query", json=query)

    if response.status_code != 200:
        raise RuntimeError("Failed to clear the search engine.")

    time.sleep(2)


class SearchEngineTest(IsolatedAsyncioTestCase):

    async def asyncSetUp(self) -> None:
        SearchEngine.term_index_name += "_test"
        self.search_engine = await get_search_engine()

        clear_search_engine(self.search_engine)

    async def test_insert_and_search_terms(self):
        """
        Test inserting and searching for terms at the search engine.
        """
        # There should be nothing in the search engine.
        suggests = await self.search_engine.search("direito")
        self.assertListEqual(suggests, list())

        # Feeding the search engine with some terms.
        terms = [
            "direito do consumidor",
            "direito do trabalhador",
            "direito das mulheres",
        ]

        for term in terms:
            await self.search_engine.insert_term(term)

        # Wait for the search engine to index the terms successfully.
        time.sleep(2)

        # Searching for the terms.
        suggests = await self.search_engine.search("direito do con")
        self.assertListEqual(suggests, ["direito do consumidor"])

        suggests = await self.search_engine.search("direito do tra")
        self.assertListEqual(suggests, ["direito do trabalhador"])

        suggests = await self.search_engine.search("direito das")
        self.assertListEqual(suggests, ["direito das mulheres"])

        suggests = await self.search_engine.search("direito")
        self.assertListEqual(sorted(suggests), sorted(terms))

        await self.search_engine.close_connections()

    def tearDown(self) -> None:
        clear_search_engine(self.search_engine)
