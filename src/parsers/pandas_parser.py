import pandas as pd

from src.utils.dictionary import get_nested_value, get_values

class DataframeHeader:
    def __init__(self) -> None:
        self._header = []
        self._subheader = []
    
    @property
    def length(self) -> int:
        return len(self._header)

    @property
    def latest_index(self) -> int:
        return self.length - 1
    
    @property
    def header(self) -> list[str]:
        return self._header
    
    @property
    def subheader(self) -> list[str]:
        return self._subheader
    
    @property
    def headers(self) -> tuple[list[str], list[str]]:
        return self._header, self._subheader
    
    def add_column(self, header: str = "", subheader: str = "") -> int:
        self._header.append(header)
        self._subheader.append(subheader)

    def add_header(self, header: str) -> None:
        self.add_column(header=header)
    
    def add_subheader(self, subheader: str) -> None:
        self.add_column(subheader=subheader)

class ColumnMap:
    def __init__(self) -> None:
        self.questions = {}
        self.choices = {}
        self.rows = {}
    
    def add_question(self, id: str, index: int, details: dict) -> None:
        self.questions[id] = (index, details)
    
    def add_choice(self, id: str, index: int) -> None:
        self.choices[id] = index
    
    def add_row(self, id: str, index: int) -> None:
        self.rows[id] = index

    def get_question_index(self, id: str) -> int:
        return self.questions[id]
    
    def get_choice_index(self, id: str) -> int:
        return self.choices[id]
    
    def get_row_index(self, id: str) -> int:
        return self.rows[id]
    
    def get_value(self, question_id: str, choice_id: str) -> dict:
        choices = self.questions[question_id][1]["answers"]["choices"]
        return next(filter(lambda choice: choice["choice_id"] == choice_id, choices))["value"]

class PandasParser:
    """Class to convert Survey data to Pandas DataFrames"""

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

    def __init__(self, survey_details: dict, survey_responses: list[dict]) -> None:
        self.responses = []
        self.header = DataframeHeader()
        self.id_map = ColumnMap()
        self.survey_details = survey_details
        self.survey_responses = survey_responses

        self.df = None
    
    def convert(self) -> pd.DataFrame:
        self._get_header()
        self._get_responses()

        self.df = pd.DataFrame(self.responses, columns=list(self.header.headers))
        
        return self.df

    def _get_header(self) -> None:
        """Get header from survey details"""

        for variable in self.STATIC_VARIABLES:
            self.header.add_header(variable)
        
        for question in self.survey_details["questions"]:
            question_id, question_text = get_values(question, "question_id", "text")
            self.id_map.add_question(question_id, self.header.length, question)

            match question["family"]:
                case "single_choice":
                    self.header.add_header(question_text)

                case "multiple_choice":
                    choices = get_nested_value(question, "answers/choices")
                    choice_id, choice_text = get_values(choices[0], "choice_id", "text")

                    self.id_map.add_choice(choice_id, self.header.length)
                    self.header.add_column(question_text, choice_text)

                    if len(choices) > 1:
                        for choice in choices[1:]:
                            choice_id, choice_text = get_values(choice, "choice_id", "text")
                            self.id_map.add_choice(choice_id, self.header.length)
                            self.header.add_subheader(choice_text)
            
                case "matrix":
                    rows = get_nested_value(question, "answers/rows")
                    row_id, row_text = get_values(rows[0], "row_id", "text")

                    self.id_map.add_row(row_id, self.header.length)
                    self.header.add_column(question_text, row_text if len(rows) > 1 else "")

                    if len(rows) > 1:
                        for row in question["answers"]["rows"][1:]:
                            row_id, row_text = get_values(row, "row_id", "text")
                            self.id_map.add_row(row_id, self.header.length)
                            self.header.add_subheader(row_text)
        
    def _get_responses(self) -> None:
        """Get responses from survey responses"""
        for response in self.survey_responses:

            # Create a new row for each response with length of header.length
            row = [None] * self.header.length

            for index, variable in enumerate(self.STATIC_VARIABLES):
                row[index] = response.get(variable, None)
                if row[index] is None:
                    row[index] = self.survey_details.get(variable, None)

            for question in response["questions"]:
                question_id = question["question_id"]
                header_index, details = self.id_map.get_question_index(question_id)

                match details["family"]:
                    case "single_choice":
                        choice_id = get_nested_value(question, "answers/0/choice_id")
                        value = self.id_map.get_value(question_id, choice_id)
                        row[header_index] = value

                    case "multiple_choice":
                        for choice in question["answers"]:
                            choice_id = choice["choice_id"]
                            index = self.id_map.get_choice_index(choice_id)
                            value = self.id_map.get_value(question_id, choice_id)
                            row[index] = value
                    
                    case "matrix":
                        for row in question["answers"]:
                            choice_id, row_id = get_values(row, "choice_id", "row_id")
                            index = self.id_map.get_row_index(row_id)
                            value = self.id_map.get_value(question_id, choice_id)
                            row[index] = value

            self.responses.append(row)

