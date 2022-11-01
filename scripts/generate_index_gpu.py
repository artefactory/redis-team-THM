import pickle

import cudf
from sentence_transformers import SentenceTransformer

from generate_index import get_papers

cdf = cudf.DataFrame(list(get_papers()))

batch = cdf[:100000].copy()

model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

vectors = model.encode(
    sentences=batch.input.values_host,
    normalize_embeddings=True,
    batch_size=64,
    show_progress_bar=True,
)

batch["vector"] = cudf.Series(vectors.tolist(), index=batch.index)


with open("embeddings_100000.pkl", "wb") as f:
    pickle.dump(batch, f)
