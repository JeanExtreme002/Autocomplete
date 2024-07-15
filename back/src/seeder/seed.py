from pathlib import Path
import asyncio
import json
import logging

from src.api.search.engine import get_search_engine


async def async_seed() -> None:
    search_engine = await get_search_engine()

    with open(Path(__file__).parent / "terms.json", encoding="UTF-8") as file:
        data = set(json.load(file))

    logging.basicConfig(level=logging.INFO)
    logging.info("Seeding the search engine...")

    for term in data:
        await search_engine.insert_term(term)

    await search_engine.close_connections()

    logging.info("Search engine seeding process completed successfully.")


def seed() -> None:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_seed())
