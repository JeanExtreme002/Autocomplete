import strawberry

from src.api.graphql.query import Query

schema = strawberry.Schema(query=Query)