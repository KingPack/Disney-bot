from typing import Dict


class ProfileParser:
    recruiter_keywords = ["recruiter", "talent", "hiring", "recruitment", "hr", "headhunter"]

    @staticmethod
    def parse_profile(text: str) -> Dict[str, bool]:
        normalized = text.lower()
        return {
            "is_recruiter": any(keyword in normalized for keyword in ProfileParser.recruiter_keywords),
        }
