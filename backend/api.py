from aredis_om import Migrator, get_redis_connection
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from thm.api import routes
from thm.config.settings import get_settings
from thm.models import Paper

config = get_settings()

app = FastAPI(
    title=config.project_name, docs_url=config.api_docs, openapi_url=config.openapi_docs
)

# TODO https://github.com/redis/redis-om-python/blob/main/docs/fastapi_integration.md
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    routes.paper_router, prefix=f"{config.api_v1_str}/paper", tags=["papers"]
)


@app.on_event("startup")
async def startup():
    Paper.Meta.database = get_redis_connection(
        url=config.get_redis_url(), decode_responses=True
    )
    Paper.Meta.global_key_prefix = "THM"
    Paper.Meta.model_key_prefix = "Paper"

    await Migrator().run()


app.mount("/data", StaticFiles(directory="thm/data"), name="data")
