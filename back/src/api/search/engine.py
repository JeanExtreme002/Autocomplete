from elasticsearch import AsyncElasticsearch
from typing import List, Tuple
import time
import requests

from src.config import Config

__all__ = ["SearchEngine", "get_search_engine"]


class SearchEngine:
    """
    Class for connecting and doing operations at the search engine.
    """

    term_index_name = "terms_index"

    def __init__(self, host: str, port: int, timeout: int = 60 * 5):
        self.base_url = f"http://{host}:{port}"

        self.client: AsyncElasticsearch = AsyncElasticsearch(self.base_url)
        self.client._verified_elasticsearch = True

        self.operations_timeout = f"{Config.ELASTIC_SEARCH_CONFIG.TIMEOUT}s"

        # Wait for Elasticsearch to become available.
        start_time = time.time()

        while (time.time() - start_time) < timeout:
            try:
                response = requests.get(
                    self.base_url + "/_cluster/health?wait_for_status=yellow&timeout=1s"
                )

                if response.status_code == 200:
                    break
            except requests.exceptions.ConnectionError:
                pass
        else:
            raise RuntimeError("Elasticsearch is not available within the timeout period.")

    async def close_connections(self):
        """
        Close all internal conections.
        """
        await self.client.close()

    async def initialize(self):
        """
        Initialize indices.
        """
        exists = await self.client.indices.exists(index=self.term_index_name)

        # Create index if it does not exist.
        if not exists:
            await self.__create_term_index()

    async def __create_term_index(self) -> None:
        """
        Create a term index into the ElasticSearch.
        """
        await self.client.indices.create(
            index=self.term_index_name,
            timeout="60s",
            body={
                "mappings": {
                    "properties": {
                        "term": {
                            "type": "completion",
                            "max_input_length": 200
                        }
                    }
                }
            },
        )

    async def get_all_terms(self, page: int = 0) -> List[str]:
        """
        Get all terms from the search engine.
        """
        offset = page * 100
        size = 100

        response = await self.client.search(
            index=self.term_index_name,
            body={"query": {"match_all": {}}},
            from_=offset, size=size,
            timeout=self.operations_timeout
        )
        return [hits["_source"]["term"] for hits in response["hits"]["hits"]]

    async def insert_term(self, term: str) -> None:
        """
        Insert a new term into the search engine.
        """
        await self.client.index(
            index=self.term_index_name, 
            document={"term": term},
            timeout=self.operations_timeout
        )

    async def insert_terms(self, *terms: Tuple[str]) -> None:
        """
        Insert multiple terms into the search engine.
        """
        index = self.term_index_name

        documents = [{"_index": index, "_source": {"term": term}} for term in terms]
        await self.client.bulk(documents, index=index, timeout=self.operations_timeout)

    async def search(self, text: str, max_results: int = 20) -> List[str]:
        """
        Search for a term.
        """
        response = await self.client.search(
            index=self.term_index_name,
            body={
                "suggest": {
                    "term_suggest": {
                        "prefix": text,
                        "completion": {"field": "term", "size": max_results},
                    }
                }
            },
            timeout=self.operations_timeout
        )
        suggestions = response["suggest"]["term_suggest"][0]["options"]

        return [suggestion["text"] for suggestion in suggestions]


search_engine_initialized = False


async def get_search_engine() -> SearchEngine:
    """
    Return an instance of the SearchEngine.
    """
    global search_engine_initialized

    search_engine = SearchEngine(
        host=Config.ELASTIC_SEARCH_CONFIG.HOST, port=Config.ELASTIC_SEARCH_CONFIG.PORT
    )

    if not search_engine_initialized:
        await search_engine.initialize()
        search_engine_initialized = True

    return search_engine
