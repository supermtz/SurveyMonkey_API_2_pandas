from src.utils.dictionary import get_values, get_nested_value
from src.parsers.answers_details_parser import AnswerDetailsAdapter

class DetailsParser:
    @classmethod
    def parse_question(cls, question: dict) -> dict:
        """Get question details"""
        question_id, family, subtype, text, answers = get_values(question, "id", "family", "subtype", "text", "answers")

        return {
            "question_id": question_id,
            "family": family,
            "subtype": subtype,
            "text": text,
            "answers": AnswerDetailsAdapter.convert(answers, family, subtype),
        }
    
    @classmethod
    def parse_questions(cls, questions: list) -> list:
        """Get questions details"""
        return [cls.parse_question(question) for question in questions]
    
    @classmethod
    def parse_survey(cls, survey: dict) -> dict:
        """Get survey details"""
        questions = []
        survey_id, pages, title = get_values(survey, "id", "pages", "headings/0/heading") 
        
        for page in pages:
            questions.extend(page["questions"])
        
        return {
            "survey_id": survey_id,
            "title": title,
            "questions": cls.parse_questions(questions),
        }