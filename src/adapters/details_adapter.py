from src.utils.dictionary_path import dictionary_path
from src.adapters.answers_details_adapter import AnswerDetailsAdapter

class DetailsAdapter:
    @classmethod
    def parse_question(cls, question: dict) -> dict:
        """Get question details"""
        return {
            "question_id": question["id"],
            "family": question["family"],
            "subtype": question["subtype"],
            "text": question["text"],
            "answers": AnswerDetailsAdapter.convert(question["answers"], question["family"], question["subtype"]),
        }
    
    @classmethod
    def parse_questions(cls, questions: list) -> list:
        """Get questions details"""
        return list(map(cls.parse_question, questions))
    
    @classmethod
    def parse_survey(cls, survey: dict) -> dict:
        """Get survey details"""
        questions = []
        
        for page in survey["pages"]:
            questions.extend(page["questions"])
        
        return {
            "survey_id": survey["id"],
            "title": dictionary_path(survey, "headings/0/heading"),
            "questions": cls.parse_questions(questions),
        }