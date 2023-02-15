from src.utils.dictionary import get_values, get_nested_value
from src.parsers.answers_response_parser import AnswersResponseAdapter

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
    def parse_question(cls, response: dict, question_details: dict) -> dict:
        """Get question details"""
        question_id, family, subtype, answers = get_values(response, "id", "family", "subtype", "answers")

        return {
            "question_id": question_id,
            "family": family,
            "subtype": subtype,
            "answers": AnswersResponseAdapter.convert(answers, question_details, family, subtype),
        }
    
    @classmethod
    def parse_questions(cls, questions: list, details: dict) -> list:
        """Get questions details"""
        parsed_questions = []
        for question in questions:
            question_id = question["id"]
            question_details = details[question_id]
            parsed_questions.append(cls.parse_question(question, question_details))
            
        return [cls.parse_question(question) for question in questions]
    
    @classmethod
    def parse_response(cls, response: dict, details: dict) -> dict:
        """Get response details"""
        parsed_response = {}

        for variable in cls.STATIC_VARIABLES:
            parsed_response[variable] = response.get(variable, None)
        
        questions = []

        for page in response["pages"]:
            questions.extend(page["questions"])
        
        parsed_response["questions"] = cls.parse_questions(questions, details)

        return parsed_response
    
    def parse_responses(cls, responses: list, details: dict) -> list:
        """Get responses details"""
        return [cls.parse_response(response, details) for response in responses]