from src.utils.dictionary import get_values, get_nested_value
from src.parsers.answers_details_parser import AnswerDetailsParser

class DetailsParser:
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
    def parse_question(cls, question: dict) -> dict:
        """Get question details"""
        question_id, family, subtype, text = get_values(question, "id", "family", "subtype", "headings/0/heading")

        return {
            "question_id": question_id,
            "family": family,
            "subtype": subtype,
            "text": text,
            "answers": AnswerDetailsParser.parse(question, family, subtype),
        }
    
    @classmethod
    def parse_questions(cls, questions: list) -> list:
        """Get questions details"""
        return [cls.parse_question(question) for question in questions]
    
    @classmethod
    def parse_survey(cls, survey: dict) -> dict:
        """Get survey details"""
        static_details = {}

        for variable in cls.STATIC_VARIABLES:
            static_details[variable] = survey.get(variable, None)

        survey_id, pages, title = get_values(survey, "id", "pages", "title") 
        
        questions = []

        for page in pages:
            questions.extend(page["questions"])
        
        return {
            "survey_id": survey_id,
            "title": title,
            **static_details,
            "questions": cls.parse_questions(questions),
        }