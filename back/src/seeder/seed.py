from pathlib import Path
import json
import logging

from src.api.search.engine import search_engine


with open(Path(__file__).parent / "terms.json") as file:
    data = set(json.load(file))

def seed() -> None:
    logging.basicConfig(level=logging.INFO)
    logging.info("Seeding the search engine...")

    for term in data:
        search_engine.insert_term(term)

    logging.info("Search engine seeding process completed successfully.")