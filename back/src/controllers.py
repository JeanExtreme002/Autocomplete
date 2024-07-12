from abc import ABC
from typing import List

from src.search.engine import SearchEngine
from src.config import ElasticSearchConfig

search_engine = SearchEngine(
    host=ElasticSearchConfig.HOST, 
    port=ElasticSearchConfig.PORT
)

class Controller(ABC):

    @staticmethod
    def get_terms(text: str) -> List[str]:
        if len(text) < 4:
            return list()

        return search_engine.search(text, max_results=ElasticSearchConfig.MAX_RESULTS)

    @staticmethod
    def create_term(term: str) -> None:
        search_engine.insert_term(term)
