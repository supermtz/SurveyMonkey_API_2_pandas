class AnswerDetailsParser:
    @classmethod
    def parse(cls, question: dict, family: str, subtype: str = "") -> list:
        answers = question.get("answers", None)
        match family:
            case "single_choice":
                return cls._parse_single_choice(answers)
            case "multiple_choice":
                return cls._parse_multiple_choice(answers)
            case "matrix":
                match subtype:
                    case "single":
                        return cls._parse_matrix_single(answers)
                    case "rating":
                        return cls._parse_matrix_rating(answers)
            case "open_ended":
                return None
            case "datetime":
                return None

    # Means static method (one for all instances of class)
    # RETURNS:
    # A list of dicts with following keys: "choice_id", "text", "value"
    @classmethod
    def _parse_single_choice(cls, answers: dict) -> list:
        choices = list(
            map(
                lambda choice: {
                    "choice_id": choice["id"],
                    "text": choice["text"],
                    "value": choice["position"],
                },
                answers["choices"],
            )
        )

        return {
            "rows": [],
            "choices": choices,
        }
    
    @classmethod
    def _parse_multiple_choice(cls, answers: dict) -> list:
        choices = list(
            map(
                lambda choice: {
                    "choice_id": choice["id"],
                    "text": choice["text"],
                    "value": choice["position"],
                },
                answers["choices"],
            )
        )

        return {
            "rows": [],
            "choices": choices,
        }

    @classmethod
    def _parse_matrix_single(cls, answers: dict) -> list:
        rows = list(
            map(lambda row: {"row_id": row["id"], "text": row["text"]}, answers["rows"])
        )
        choices = list(
            map(
                lambda choice: {
                    "choice_id": choice["id"],
                    "text": choice["text"],
                    "value": choice["position"],
                },
                answers["choices"],
            )
        )

        return {
            "rows": rows,
            "choices": choices,
        }

    @classmethod
    def _parse_matrix_rating(cls, answers: dict) -> list:
        rows = list(
            map(lambda row: {"row_id": row["id"], "text": row["text"]}, answers["rows"])
        )
        choices = list(
            map(
                lambda choice: {
                    "choice_id": choice["id"],
                    "text": choice["text"],
                    "value": choice["weight"],
                },
                answers["choices"],
            )
        )

        return {
            "rows": rows,
            "choices": choices,
        }
