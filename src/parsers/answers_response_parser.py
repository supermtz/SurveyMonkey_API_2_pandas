from src.utils.dictionary import get_values, get_nested_value


class AnswersResponseParser:
    """Adapter for response Data"""

    @classmethod
    def parse(
        cls, answers: list[dict], details: dict, family: str, subtype: str = ""
    ) -> dict:
        """Main parser"""
        match family:
            case "single_choice":
                return cls._parse_single_choice(answers, details)
            case "multiple_choice":
                return cls._parse_multiple_choice(answers, details)
            case "matrix":
                match subtype:
                    case "single":
                        return cls._parse_matrix_single(answers, details)
                    case "rating":
                        return cls._parse_matrix_rating(answers, details)
                    
    @classmethod
    def _parse_single_choice(cls, answers: dict, details: dict) -> dict:
        """Parse single choice response"""
        choice_id = get_values(answers, "0/choice_id")
        
        
        
