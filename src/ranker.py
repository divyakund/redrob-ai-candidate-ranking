import pandas as pd
from tqdm import tqdm

from src.candidate_builder import CandidateBuilder
from src.semantic_match import SemanticMatcher
from src.scorer import CandidateScorer


class CandidateRanker:

    def __init__(self):
        self.matcher = SemanticMatcher()
        self.scorer = CandidateScorer()

    def rank(self, df, job_description, limit=1000):

        print(f"\nRanking first {limit} candidates...\n")

        candidates = df.head(limit).copy()

        candidate_texts = []

        for _, row in tqdm(
            candidates.iterrows(),
            total=len(candidates),
            desc="Building Documents"
        ):
            candidate_texts.append(
                CandidateBuilder.build(row)
            )

        # Semantic similarity
        jd_embedding = self.matcher.encode_job_description(job_description)

        candidate_embeddings = self.matcher.encode_candidates(candidate_texts)

        semantic_scores = self.matcher.similarity_scores(
            jd_embedding,
            candidate_embeddings
        )

        important = {
            "Python",
            "NLP",
            "Fine-tuning LLMs",
            "LoRA",
            "QLoRA",
            "PEFT",
            "Milvus",
            "Pinecone",
            "Qdrant",
            "Weaviate",
            "FAISS",
            "Elasticsearch",
            "OpenSearch",
            "Sentence Transformers",
            "Embeddings"
        }

        results = []

        for i, (_, row) in enumerate(candidates.iterrows()):

            scores = self.scorer.final_score(
                semantic_scores[i],
                row
            )

            ai_skill_count = 0

            for skill in row["skills"]:
                if skill["name"] in important:
                    ai_skill_count += 1

            results.append({

                "candidate_id": row["candidate_id"],

                "title": row["profile"]["current_title"],

                "years": row["profile"]["years_of_experience"],

                "response_rate": row["redrob_signals"]["recruiter_response_rate"],

                "ai_skill_count": ai_skill_count,

                "semantic": round(scores["semantic"], 4),

                "career": round(scores["career"], 4),

                "skills": round(scores["skills"], 4),

                "behavior": round(scores["behavior"], 4),

                "experience": round(scores["experience"], 4),

                "final_score": round(scores["final"], 4)

            })

        results = pd.DataFrame(results)

        results = results.sort_values(
            "final_score",
            ascending=False
        )

        return results