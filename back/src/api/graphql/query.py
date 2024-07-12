from typing import List, Optional
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
    def all_terms(self, page: Optional[int] = 0) -> List[str]:
        return search_engine.get_all_terms(page=page)

    @strawberry.field
    def search_terms(self, text: str) -> List[str]:
        if len(text) < 4:
            return list()

        return search_engine.search(text, max_results=ElasticSearchConfig.MAX_RESULTS)
