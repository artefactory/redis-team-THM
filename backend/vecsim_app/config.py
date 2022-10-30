import os

# FIXME Pydantic Settings file
PROJECT_NAME = "vecsim_app"
API_DOCS = "/api/docs"
OPENAPI_DOCS = "/api/openapi.json"
INDEX_NAME = "papers"
INDEX_TYPE = os.environ.get("VECSIM_INDEX_TYPE", "HNSW")
REDIS_HOST = "redis-13927.c21977.us-east-1-1.ec2.cloud.rlrcp.com"
# os.environ.get("REDIS_HOST", "redis-vector-db")
REDIS_PORT = 13927
# os.environ.get("REDIS_PORT", 6379)
REDIS_DB = "arxiv-db"
# os.environ.get("REDIS_DB", 0)
REDIS_PASSWORD = "ZbZuFbYa9w3FQaafEU6yTM5fADXBhPS5"
# os.environ.get("REDIS_PASSWORD", "testing123")

REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
os.environ["REDIS_DATA_URL"] = REDIS_URL
os.environ["REDIS_OM_URL"] = REDIS_URL
API_V1_STR = "/api/v1"
DATA_LOCATION = os.environ.get("DATA_LOCATION", "../datascience")
