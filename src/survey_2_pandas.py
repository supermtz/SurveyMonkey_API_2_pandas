import pandas as pd

class Survey_2_Pandas:
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
        self.header = []
        self.subheader = []
        self.responses = []
        self.questions_map = {}
        self.choices_map = {}
        self.rows_map = {}
        self.survey_details = survey_details
        self.survey_responses = survey_responses

        self.df = None
    
    def convert(self) -> pd.DataFrame:
        self._get_header()
        self._get_responses()

        self.df = pd.DataFrame([self.header, self.subheader], columns=self.header).append(self.responses, ignore_index=True)

        return self.df

    def _get_header(self) -> None:
        """Get header from survey details"""
        self.header.extend(self.STATIC_VARIABLES)
        self.subheader.extend([""] * len(self.header))
        
        for question in self.survey_details["questions"]:
            match question["family"]:
                case "single_choice":
                    self.questions_map[question["question_id"]] = len(self.header)
                    self.header.append(question["text"])
                    self.subheader.append("")
                case "multiple_choice":
                    self.questions_map[question["question_id"]] = len(self.header)
                    self.choices_map[question["answers"]["choices"][0]["id"]] = len(self.header)
                    self.header.append(question["text"])
                    self.subheader.append(question["answers"]["choices"][0]["text"])
                    for choice in question["answers"]["choices"][1:]:
                        self.choices_map[choice["id"]] = len(self.header)
                        self.header.append("")
                        self.subheader.append(choice["text"])
                case "matrix":
                    self.questions_map[question["question_id"]] = len(self.header)
                    self.rows_map[question["answers"]["rows"][0]["id"]] = len(self.header)
                    self.header.append(question["text"])
                    if len(question["answers"]["rows"]) == 1:
                        self.subheader.append("")
                    elif len(question["answers"]["rows"]) > 1:
                        self.subheader.append(question["answers"]["rows"][0]["text"])
                        for row in question["answers"]["rows"][1:]:
                            self.rows_map[row["id"]] = len(self.header)
                            self.header.append("")
                            self.subheader.append(row["text"])
    
    def _get_responses(self) -> None:
        """Get responses from survey responses"""
        for response in self.survey_responses["data"]:
            row = []

            for variable in self.STATIC_VARIABLES:
                row.append(response.get(variable, ""))
            for question in response["questions"]:
                match question["family"]:
                    case "single_choice":
                        row[self.questions_map[question["id"]]] = question["answers"]["choices"]["value"]
                    case "multiple_choice":
                        for choice in question["answers"]["choices"]:
                            row[self.choices_map[choice["id"]]] = choice["value"]
                    case "matrix":
                        for row in question["answers"]["rows"]:
                            row[self.rows_map[row["id"]]] = row["value"]

            self.responses.append(row)

