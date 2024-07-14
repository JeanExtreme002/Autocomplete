from fastapi import APIRouter, Depends, status
from strawberry.fastapi import GraphQLRouter

from src.api.graphql.schema import schema
from src.api.search.engine import get_search_engine

async def get_context(search_engine=Depends(get_search_engine)):
    return {"search_engine": search_engine}

graphql_app = GraphQLRouter(schema, context_getter=get_context)

router = APIRouter()
router.include_router(graphql_app, prefix="/graphql")

@router.get("/", status_code=status.HTTP_200_OK)
async def index():
    return {"status": "alive"}

