from src.data_loader import DataLoader
from src.ranker import CandidateRanker
from src.submission import SubmissionGenerator

loader = DataLoader()

df = loader.load_candidates()

jd = loader.load_job_description()

ranker = CandidateRanker()

results = ranker.rank(
    df,
    jd,
    limit=100000
)

submission = SubmissionGenerator().generate(
    results,
    top_n=100
)

print("\n======================")
print("TOP 10 SUBMISSION")
print("======================")

print(submission.head(10))