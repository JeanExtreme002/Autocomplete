from elasticsearch import Elasticsearch
from typing import List


class SearchEngine():
    """
    Class for connecting and doing operations at the search engine. 
    """
    term_index_name = "term_index"

    def __init__(self, host: str, port: int):
        self.client = Elasticsearch(f"http://{host}:{port}")
        self.client._verified_elasticsearch = True

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