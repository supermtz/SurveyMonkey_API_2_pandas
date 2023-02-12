class AnswerDetailsAdapter:
    @classmethod
    def convert(cls, answers: dict, family: str, subtype: str = "") -> list:
        match family:
            case "single_choice":
                return cls.convert_single_choice(answers)
            case "matrix":
                match subtype:
                    case "single":
                        return cls.convert_matrix_single(answers)
                    case "rating":
                        return cls.convert_matrix_rating(answers)
            case "multiple_choice":
                return cls.convert_multiple_choice(answers)

    # Means static method (one for all instances of class)
    # RETURNS:
    # A list of dicts with following keys: "choice_id", "text", "value"
    @classmethod
    def convert_single_choice(cls, answers: dict) -> list:
        choices = answers["choices"]
        return list(
            map(
                lambda choice: {
                    "choice_id": choice["id"],
                    "text": choice["text"],
                    "value": choice["position"],
                },
                choices,
            )
        )

    @classmethod
    def convert_matrix_single(cls, answers: dict) -> list:
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
    def convert_matrix_rating(cls, answers: dict) -> list:
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

    @classmethod
    def convert_multiple_choice(cls, answers: dict) -> list:
        choices = answers["choices"]
        return list(
            map(
                lambda choice: {
                    "choice_id": choice["id"],
                    "text": choice["text"],
                    "value": choice["position"],
                },
                choices,
            )
        )
