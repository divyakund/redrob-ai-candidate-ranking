class CandidateBuilder:

    @staticmethod
    def build(candidate):

        profile = candidate["profile"]

        sections = []

        # Profile
        sections.append(profile.get("headline", ""))
        sections.append(profile.get("summary", ""))

        # Career History
        for job in candidate["career_history"]:

            sections.append(job.get("title", ""))

            sections.append(job.get("description", ""))

        # Skills
        skills = []

        for skill in candidate["skills"]:
            skills.append(skill["name"])

        sections.append("Skills : " + ", ".join(skills))

        # Education
        education = []

        for edu in candidate["education"]:

            education.append(
                f"{edu.get('degree','')} "
                f"{edu.get('field_of_study','')}"
            )

        sections.append("Education : " + ", ".join(education))

        return "\n".join(sections)