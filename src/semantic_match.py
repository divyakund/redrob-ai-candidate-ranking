from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm


class SemanticMatcher:

    def __init__(self):

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print("Model Ready!")

    def encode_job_description(self, jd):

        return self.model.encode(
            jd,
            normalize_embeddings=True
        )

    def encode_candidates(self,
                          candidate_texts,
                          batch_size=128):

        return self.model.encode(
            candidate_texts,
            batch_size=batch_size,
            show_progress_bar=True,
            normalize_embeddings=True
        )

    def similarity_scores(
            self,
            jd_embedding,
            candidate_embeddings
    ):

        scores = cosine_similarity(
            [jd_embedding],
            candidate_embeddings
        )[0]

        return scores