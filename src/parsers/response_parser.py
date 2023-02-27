from src.utils.dictionary import get_values, get_nested_value
from src.parsers.answers_response_parser import AnswersResponseParser

class ResponseParser:
    STATIC_VARIABLES = [
        "recipient_id",
        "collector_id",
        "date_created",
        "date_modified",
        "ip_address",
        "email_address",
        "first_name",
        "last_name",
    ]

    @classmethod
    def parse_question(cls, response: dict) -> dict:
        """Get question details"""
        question_id, answers = get_values(response, "id", "answers")

        return {
            "question_id": question_id,
            "answers": AnswersResponseParser.parse(answers),
        }
    
    @classmethod
    def parse_response(cls, response: dict) -> dict:
        """Get response details"""
        parsed_response = {}

        for variable in cls.STATIC_VARIABLES:
            parsed_response[variable] = response.get(variable, None)
        
        questions = []
        
        for page in response["pages"]:
            questions.extend(page["questions"])

        parsed_response["questions"] = [cls.parse_question(question) for question in questions]

        return parsed_response
    
    @classmethod
    def parse_responses(cls, responses: list) -> list:
        """Get responses details"""
        return [cls.parse_response(response) for response in responses]