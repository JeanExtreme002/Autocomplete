from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from typing import List
import time
import requests

from src.config import ElasticSearchConfig

__all__ = ["search_engine"]


class SearchEngine():
    """
    Class for connecting and doing operations at the search engine. 
    """
    term_index_name = "term_index"

    def __init__(self, host: str, port: int, timeout: int = 60 * 5):
        self.client = Elasticsearch(f"http://{host}:{port}")
        self.client._verified_elasticsearch = True

        # Wait for Elasticsearch to become available.
        start_time = time.time()

        while (time.time() - start_time) < timeout:
            try:
                response = requests.get(f"http://{host}:{port}/_cluster/health?wait_for_status=yellow&timeout=1s")

                if response.status_code == 200:
                    break
            except requests.exceptions.ConnectionError:
                pass
        else:
            raise RuntimeError("Elasticsearch is not available within the timeout period.")

        # Create index if it does not exist.
        if not self.client.indices.exists(index=self.term_index_name):
            self.__create_term_index()

    def __create_term_index(self) -> None:
        """
        Create a term index into the ElasticSearch.
        """
        self.client.indices.create(
            index=self.term_index_name, 
            body={
                "mappings": {
                    "properties": {
                        "term": {
                            "type": "completion"
                        }
                    }
                }
            }
        )

    def get_all_terms(self, page: int = 0) -> List[str]:
        """
        Get all terms from the search engine.
        """
        offset = page * 100
        size = 100

        response = self.client.search(
            index=self.term_index_name,
            body={
                "query": {"match_all": {}}
            },
            from_=offset,
            size=size
        )
        return [hits["_source"]["term"] for hits in response["hits"]["hits"]]

    def insert_term(self, term: str) -> None:
        """
        Insert a new term into the search engine.
        """
        self.client.index(
            index=self.term_index_name,
            document={"term": term}
        )

    def insert_terms(self, *terms: str) -> None:
        """
        Insert multiple terms into the search engine.
        """
        index = self.term_index_name

        documents = [{"_index": index, "_source": {"term": term}} for term in terms]
        bulk(self.client, documents, index=index, raise_on_error=True)

    def search(self, text: str, max_results: int = 20) -> List[str]:
        """
        Search for a term.
        """
        response = self.client.search(
            index=self.term_index_name, 
            body={
                "suggest": {
                    "term_suggest" : {
                        "prefix" : text,
                        "completion" : {
                            "field" : "term",
                            "size": max_results
                        }
                    }
                }
            }
        )
        suggestions = response["suggest"]["term_suggest"][0]["options"]
        
        return [suggestion["text"] for suggestion in suggestions]


search_engine = SearchEngine(
    host=ElasticSearchConfig.HOST, 
    port=ElasticSearchConfig.PORT
)