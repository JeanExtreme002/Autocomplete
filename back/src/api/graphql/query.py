from typing import List, Optional
import strawberry

from src.config import ElasticSearchConfig


@strawberry.type
class Query:

    @strawberry.field
    async def all_terms(self, info: strawberry.Info, page: Optional[int] = 0) -> List[str]:
        search_engine = info.context["search_engine"]

        results = await search_engine.get_all_terms(page=page)
        await search_engine.close_connections()

        return results

    @strawberry.field
    async def search_terms(self, info: strawberry.Info, text: str) -> List[str]:
        if len(text) < 4:
            return list()

        search_engine = info.context["search_engine"]

        results = await search_engine.search(text, max_results=ElasticSearchConfig.MAX_RESULTS)
        await search_engine.close_connections()

        return results
