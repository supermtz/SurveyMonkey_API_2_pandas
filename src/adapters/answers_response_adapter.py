"""Adapter for response Data"""


class AnswersResponseAdapter:
    """Adapter for response Data"""

    @classmethod
    def parse(
        cls, response: dict, details: dict, family: str, subtype: str = ""
    ) -> dict:
        """Main parser"""
