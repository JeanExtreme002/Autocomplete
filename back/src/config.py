import dotenv
import os

dotenv.load_dotenv()


class ElasticSearchConfig:
    """
    ElasticSearch configuration.
    """
    HOST = os.getenv("ELASTICSEARCH_HOST", "localhost")
    PORT = int(os.getenv("ELASTICSEARCH_PORT", "9200"))
    MAX_RESULTS = int(os.getenv("ELASTICSEARCH_MAX_RESULTS", "20"))


class Config:
    """
    Base configuration.
    """

    ENVIRONMENT = os.getenv("ENVIRONMENT", "DEV")
    DEBUG = ENVIRONMENT == "DEV"

    HOST = os.getenv("APPLICATION_HOST", "127.0.0.1")
    PORT = int(os.getenv("APPLICATION_PORT", "5000"))
    WORKERS_COUNT = int(os.getenv("WORKERS_COUNT", "1"))
    RELOAD = os.getenv("RELOAD", "true").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").lower()

    APPLICATION_ROOT = os.getenv("APPLICATION_ROOT", "")
