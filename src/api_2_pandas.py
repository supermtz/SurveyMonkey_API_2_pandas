import asyncio
import pandas as pd
from src.surveymonkey_api_client import SurveyMonkeyAPIClient
from src.adapters.details_adapter import DetailsAdapter
from src.adapters.answers_response_adapter import AnswersResponseAdapter
from src.survey_2_pandas import Survey2Pandas

class API2Pandas:
    def __init__(self, api_token: str, survey_ids = None) -> None:
        self.client = SurveyMonkeyAPIClient(api_token)
        self.survey_ids = survey_ids if survey_ids else []
        self.survey_details = {}
        self.survey_responses = {}

        self.df = None
    
    def search_surveys(self, amount = 50, search_str: str = None) -> None:
        """Find surveys by title"""
        surveys = self.client.get_surveys(amount, search_str)
        self.survey_ids = [survey["id"] for survey in surveys]

    async def get_survey_details(self, survey_id: str) -> dict:
        """Get survey details"""
        survey_details = await self.client.get_survey_details(survey_id)
        return DetailsAdapter.parse_survey(survey_details)

    async def get_responses(self, survey_id: str, amount = 50, custom_variables: dict = None) -> list:
        """Get survey responses"""
        responses = await self.client.get_responses(survey_id, amount, custom_variables)
        ret_responses = []
        for response in responses:
            ret_responses.append(AnswersResponseAdapter.parse(response))
        return ret_responses

    def collect(self, amount = 50, custom_variables: dict = None) -> None:
        """Collect survey details and responses"""
        details = self.collect_details()
        responses = self.collect_responses(amount, custom_variables)
        asyncio.run(asyncio.gather(details, responses))
        self.close()

    async def collect_details(self) -> None:
        """Collect survey details and responses"""
        co_survey_details = {survey_id: self.get_survey_details(survey_id) for survey_id in self.survey_ids}
        for survey_id, details in co_survey_details.items():
            self.survey_details[survey_id] = await details

    async def collect_responses(self, amount = 50, custom_variables: dict = None) -> None:
        """Collect survey details and responses"""
        co_survey_responses = {survey_id: self.get_responses(survey_id, amount, custom_variables) for survey_id in self.survey_ids}
        for survey_id, responses in co_survey_responses.items():
            self.survey_responses[survey_id] = await responses

    def run(self, response_amount = 50, custom_variables: dict = None) -> pd.DataFrame:
        """Run the parser"""
        self.collect(response_amount, custom_variables)
        self.close()
        parser = Survey2Pandas(self.survey_details, self.survey_responses)
        self.df = parser.convert()
        return self.df

    def close(self) -> None:
        """Close the client session"""
        self.client.close()