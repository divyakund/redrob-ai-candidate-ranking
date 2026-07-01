import pandas as pd
from docx import Document


class DataLoader:

    def __init__(self,
                 candidate_path="candidates.jsonl",
                 jd_path="job_description.docx"):

        self.candidate_path = candidate_path
        self.jd_path = jd_path

    def load_candidates(self):

        print("Loading candidate dataset...")

        df = pd.read_json(self.candidate_path, lines=True)

        print(f"Loaded {len(df)} candidates")

        return df

    def load_job_description(self):

        doc = Document(self.jd_path)

        jd = []

        for para in doc.paragraphs:

            if para.text.strip():
                jd.append(para.text.strip())

        return "\n".join(jd)