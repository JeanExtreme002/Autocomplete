from pathlib import Path
import json

from src.api.search.engine import SearchEngine
from src.config import ElasticSearchConfig

search_engine = SearchEngine(
    host=ElasticSearchConfig.HOST, 
    port=ElasticSearchConfig.PORT
)

with open(Path(__file__).parent / "terms.json") as file:
    data = set(json.load(file))

def seed() -> None:
    for term in data:
        search_engine.insert_term(term)