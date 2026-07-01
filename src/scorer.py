class CandidateScorer:

    IMPORTANT_SKILLS = {
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

    def experience_score(self, candidate):

        years = candidate["profile"]["years_of_experience"]

        if 5 <= years <= 9:
            return 1.0
        elif 4 <= years < 5:
            return 0.85
        elif 9 < years <= 12:
            return 0.85
        elif years > 12:
            return 0.70
        else:
            return 0.50

    def skills_score(self, candidate):

        skills = {s["name"] for s in candidate["skills"]}

        matches = skills.intersection(self.IMPORTANT_SKILLS)

        return len(matches) / len(self.IMPORTANT_SKILLS)

    def career_score(self, candidate):

        score = 0

        positive_phrases = [
            "production",
            "deployed",
            "deployed models",
            "real-time",
            "recommendation",
            "ranking",
            "retrieval",
            "semantic search",
            "vector database",
            "embeddings",
            "fine tuning",
            "fine-tuning",
            "llm",
            "transformer",
            "search engine",
            "evaluation",
            "a/b testing",
            "online inference",
            "offline evaluation",
            "ml pipeline",
            "feature engineering",
            "airflow",
            "spark",
            "pytorch",
            "tensorflow"
        ]

        for job in candidate["career_history"]:

            text = (
                job.get("title", "") +
                " " +
                job.get("description", "")
            ).lower()

            matches = 0

            for phrase in positive_phrases:
                if phrase in text:
                    matches += 1

            if job.get("is_current", False):
                matches += 2

            score += matches

        return min(score / 20, 1)

    def behavior_score(self, candidate):

        s = candidate["redrob_signals"]

        score = 0

        score += min(s["profile_completeness_score"] / 100, 1) * 0.20
        score += min(s["github_activity_score"] / 10, 1) * 0.20
        score += s["recruiter_response_rate"] * 0.20
        score += s["interview_completion_rate"] * 0.20
        score += min(s["saved_by_recruiters_30d"] / 10, 1) * 0.10

        if s["open_to_work_flag"]:
            score += 0.10

        return min(score, 1)

    def final_score(self, semantic, candidate):

        experience = self.experience_score(candidate)
        skills = self.skills_score(candidate)
        career = self.career_score(candidate)
        behavior = self.behavior_score(candidate)

        final = (
            semantic * 0.40 +
            career * 0.25 +
            skills * 0.15 +
            behavior * 0.15 +
            experience * 0.05
        )

        return {
            "semantic": semantic,
            "career": career,
            "skills": skills,
            "behavior": behavior,
            "experience": experience,
            "final": final
        }