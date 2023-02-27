from src.utils.dictionary import get_values, get_nested_value


class AnswersResponseParser:
    """Adapter for response Data"""

    @classmethod
    def parse(
        cls, answers: list[dict]
    ) -> dict:
        return list(
            map(
                lambda answer: {
                    "row_id": answer.get("row_id", ""),
                    "choice_id": answer.get("choice_id", ""),
                },
                answers,
            )
        )
    