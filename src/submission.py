import pandas as pd


class SubmissionGenerator:

    def generate_reason(self, row):
        return (
            f"{row['title']} with "
            f"{row['years']:.1f} yrs; "
            f"{row['ai_skill_count']} AI core skills; "
            f"response rate {row['response_rate']:.2f}."
        )

    def generate(self, ranked_df, top_n=100):

        top = ranked_df.head(top_n).copy()

        top["rank"] = range(1, len(top) + 1)

        top["reasoning"] = top.apply(
            self.generate_reason,
            axis=1
        )

        submission = top[
            [
                "candidate_id",
                "rank",
                "final_score",
                "reasoning"
            ]
        ].copy()

        submission.rename(
            columns={"final_score": "score"},
            inplace=True
        )

        submission.to_csv(
            "output/submission.csv",
            index=False
        )

        print("\nSubmission saved to output/submission.csv")

        return submission