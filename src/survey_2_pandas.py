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
        return self.get_length() - 1
    
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
    
    def add_question(self, id: str, index: int) -> None:
        self.questions[id] = index
    
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

class Survey2Pandas:
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

    def __init__(self, survey_details: dict, survey_responses: dict) -> None:
        self.responses = []
        self.header = DataframeHeader()
        self.id_map = ColumnMap()
        self.survey_details = survey_details
        self.survey_responses = survey_responses

        self.df = None
    
    def convert(self) -> pd.DataFrame:
        self._get_header()
        self._get_responses()

        self.df = pd.DataFrame(columns=self.header.headers).append(self.responses, ignore_index=True)

        return self.df

    def _get_header(self) -> None:
        """Get header from survey details"""

        for variable in self.STATIC_VARIABLES:
            self.header.add_header(variable)
        
        for question in self.survey_details["questions"]:
            match question["family"]:
                case "single_choice":
                    id, text = get_values(question, "question_id", "text")

                    self.header.add_header(text)
                    self.id_map.add_question(id, self.header.latest_index)

                case "multiple_choice":
                    choices = get_nested_value(question, "answers/choices")
                    question_id, question_text = get_values(question, "question_id", "text")
                    choice_id, choice_text = get_values(choice[0], "id", "text")

                    self.header.add_column(question_text, choice_text)
                    self.id_map.add_question(question_id, self.header.latest_index)
                    self.id_map.add_choice(choice_id, self.header.latest_index)

                    if len(choices) > 1:
                        for choice in choices[1:]:
                            choice_id, choice_text = get_values(choice, "id", "text")
                            self.header.add_subheader(choice_text)
                            self.id_map.add_choice(choice_id, self.header.latest_index)
            
                case "matrix":
                    rows = get_nested_value(question, "answers/rows")
                    question_id, question_text = get_values(question, "question_id", "text")
                    row_id, row_text = get_values(rows[0], "id", "text")

                    self.header.add_column(question_text, row_text if len(rows) > 1 else "")

                    self.id_map.add_question(question_id, self.header.latest_index)
                    self.id_map.add_row(row_id, self.header.latest_index)

                    if len(rows) > 1:
                        for row in question["answers"]["rows"][1:]:
                            row_id, row_text = get_values(row, "id", "text")
                            self.header.add_subheader(row_text)
                            self.id_map.add_row(row_id, self.header.latest_index)
        
    def _get_responses(self) -> None:
        """Get responses from survey responses"""
        for response in self.survey_responses["data"]:

            # Create a new row for each response with length of header.length
            row = [None] * self.header.length

            for variable in self.STATIC_VARIABLES:
                index = self.id_map.get_question_index(variable)
                row[index] = response.get(variable, None)

            for question in response["questions"]:
                match question["family"]:
                    case "single_choice":
                        id, value = get_values(question, "id", "answers/choices/value")
                        index = self.id_map.get_question_index(id)
                        row[index] = value

                    case "multiple_choice":
                        choices = get_nested_value(question, "answers/choices")
                        for choice in choices:
                            id, value = get_values(choice, "id", "value")
                            index = self.id_map.get_choice_index(id)
                            row[index] = value
                    
                    case "matrix":
                        for row in question["answers"]["rows"]:
                            id, value = get_values(row, "id", "value")
                            index = self.id_map.get_row_index(id)
                            row[id] = value

            self.responses.append(row)

