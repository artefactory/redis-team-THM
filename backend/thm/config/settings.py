from pydantic import BaseSettings


class Settings(BaseSettings):
    project_name: str = "thm"
    api_docs: str = "/api/docs"
    openapi_docs: str = "/api/openapi.json"
    index_name: str = "papers"
    index_type: str = "HNSW"
    redis_host: str
    redis_port: int
    redis_db: str
    redis_password: str
    api_v1_str: str = "/api/v1"
    data_location: str

    def get_redis_url(self):
        return f"redis://default:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"


def get_settings():
    return Settings(_env_file="thm/config/prod.env")
    # contact Michel for the gitignored file
