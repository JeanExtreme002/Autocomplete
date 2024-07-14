import strawberry


@strawberry.type
class Mutation:

    @strawberry.field
    async def create_term(self, info: strawberry.Info, term: str) -> None:
        search_engine = info.context["search_engine"]
        search_engine.insert_term(term)