from docarray import Document, DocumentArray

from backend.thm.config.settings import get_settings

config = get_settings()

with DocumentArray(
    storage="redis",
    config={
        "n_dim": 128,
        "index_name": "papers",
        "host": config.redis_host,
        "port": config.redis_port,
        "redis_config": {"password": config.redis_password},
    },
) as da:
    da.extend([Document() for _ in range(1000)])

da2 = DocumentArray(
    storage="redis",
    config={
        "n_dim": 128,
        "index_name": "idx",
    },
)

da2.summary()
