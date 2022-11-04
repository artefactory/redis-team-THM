from os import getenv

from loguru import logger
from pydantic import BaseSettings


class Settings(BaseSettings):
    project_name: str = "THM API"
    version: str = "1.0.0"
    api_docs: str = "/api/docs"
    openapi_docs: str = "/api/openapi.json"
    index_name: str = "papers"
    index_type: str = "HNSW"
    api_v1_str: str = "/api/v1"
    data_location: str = "../data"
    year_pattern: str = "(19|20[0-9]{2})"
    embeddings_path: str = "../datascience/arxiv_embeddings_10000.pkl"
    model_name: str = "sentence-transformers/all-MiniLM-L12-v2"
    redis_host: str
    redis_port: int
    redis_db: str
    redis_password: str
    description: str = """
THM API helps you search arXiv using vector embeddings
```
+-------------------+      +----------------+
|                   |      |                |
|  Redis            +<-----+  ETL CLI       |
|                   |      |                |
+--------+----------+      +----------------+
         ^
         |  reads search index
+--------+----------+
|                   |
|  FastAPI          |
|                   |
+--------+----------+
         ^
         |  calls backend
+--------+----------+      +---------------------+
|                   |      |                     |
|  THM CLI          +----->+  arxiv.org          |
|                   |      |  wolfram.alpha.com  |
+-------------------+      +---------------------+
"""

    def get_redis_url(self):
        redis_host = getenv("REDIS_HOST", self.redis_host)
        redis_port = getenv("REDIS_PORT", self.redis_port)
        redis_db = getenv("REDIS_DB", self.redis_db)
        redis_password = getenv("REDIS_PASSWORD", self.redis_password)
        return f"redis://default:{redis_password}@{redis_host}:{redis_port}/{redis_db}"


def get_settings():
    return Settings(_env_file="../backend/thm/config/prod.env")
    # contact Michel for the gitignored file
