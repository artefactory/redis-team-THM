import os

# FIXME Pydantic Settings file
PROJECT_NAME = "vecsim_app"
API_DOCS = "/api/docs"
OPENAPI_DOCS = "/api/openapi.json"
INDEX_NAME = "papers"
INDEX_TYPE = os.environ.get("VECSIM_INDEX_TYPE", "HNSW")
REDIS_HOST = "redis-18742.c226.eu-west-1-3.ec2.cloud.redislabs.com"
# os.environ.get("REDIS_HOST", "redis-vector-db")
REDIS_PORT = 18742
# os.environ.get("REDIS_PORT", 6379)
REDIS_DB = "Michel-free-db"
# os.environ.get("REDIS_DB", 0)
REDIS_PASSWORD = "PtGSdcULLsIImHKMh6jYIeIcpZ2w7Vrl"
# os.environ.get("REDIS_PASSWORD", "testing123")

REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
os.environ["REDIS_DATA_URL"] = REDIS_URL
os.environ["REDIS_OM_URL"] = REDIS_URL
API_V1_STR = "/api/v1"
DATA_LOCATION = os.environ.get("DATA_LOCATION", "../datascience")
