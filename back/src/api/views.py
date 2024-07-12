from fastapi import APIRouter, status
from strawberry.fastapi import GraphQLRouter

from src.api.graphql.schema import schema

graphql_app = GraphQLRouter(schema)

router = APIRouter()
router.include_router(graphql_app, prefix="/graphql")

@router.get("/", status_code=status.HTTP_200_OK)
def index():
    return {"status": "alive"}

