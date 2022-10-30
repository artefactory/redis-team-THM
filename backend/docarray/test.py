from docarray import DocumentArray, Document

with DocumentArray(
    storage='redis',
    config={
        'n_dim': 128,
        'index_name': 'paper_vector',
        'host': 'redis-13927.c21977.us-east-1-1.ec2.cloud.rlrcp.com',
        'port': 13927,
        'redis_config': {
            'password': 'ZbZuFbYa9w3FQaafEU6yTM5fADXBhPS5'
        }
    },
) as da:
    da.extend([Document() for _ in range(1000)])

da2 = DocumentArray(
    storage='redis',
    config={
        'n_dim': 128,
        'index_name': 'idx',
    },
)

da2.summary()
