import pandas as pd

df = pd.read_csv("output/submission.csv")

print("Rows:", len(df))
print("Duplicate IDs:", df["candidate_id"].duplicated().sum())
print("Missing values:\n", df.isnull().sum())