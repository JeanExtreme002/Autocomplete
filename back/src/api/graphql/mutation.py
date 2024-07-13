import strawberry

from src.api.search.engine import search_engine


@strawberry.type
class Mutation:

    @strawberry.field
    async def create_term(self, term: str) -> None:
        search_engine.insert_term(term)