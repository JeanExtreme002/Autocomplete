import strawberry

from src.api.search.engine import SearchEngine
from src.config import ElasticSearchConfig

search_engine = SearchEngine(
    host=ElasticSearchConfig.HOST, 
    port=ElasticSearchConfig.PORT
)

@strawberry.type
class Mutation:

    @strawberry.field
    def create_term(self, term: str) -> None:
        search_engine.insert_term(term)