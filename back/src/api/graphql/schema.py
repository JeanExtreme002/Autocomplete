import strawberry

from src.api.graphql.query import Query
from src.api.graphql.mutation import Mutation

schema = strawberry.Schema(query=Query, mutation=Mutation)
