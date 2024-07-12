from typing import List
import strawberry

from src.api.search.engine import SearchEngine
from src.config import ElasticSearchConfig

search_engine = SearchEngine(
    host=ElasticSearchConfig.HOST, 
    port=ElasticSearchConfig.PORT
)

@strawberry.type
class Query:

    @strawberry.field
    def get_terms(self, text: str) -> List[str]:
        if len(text) < 4:
            return list()

        return search_engine.search(text, max_results=ElasticSearchConfig.MAX_RESULTS)

    @strawberry.field
    def create_term(self, term: str) -> None:
        search_engine.insert_term(term.term)