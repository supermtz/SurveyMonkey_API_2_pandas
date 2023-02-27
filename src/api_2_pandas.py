from concurrent.futures import ProcessPoolExecutor
import asyncio as aio
import pandas as pd

from src.utils.dictionary import get_values, get_nested_value
from src.API_client import SurveyMonkeyAPIClient
from src.parsers import DetailsParser, ResponseParser, PandasParser

class API2Pandas:
    def __init__(self, api_token: str, survey_ids: list = None) -> None:
        self.client = SurveyMonkeyAPIClient(api_token)
        self.survey_ids = survey_ids if survey_ids else []
        self.dfs = {}

    def search_surveys(self, amount = 50, search_str: str = None) -> None:
        """Find surveys by title"""
        surveys = aio.run(self.client.get_surveys(amount, search_str))
        self.survey_ids = [survey["id"] for survey in surveys]
        return self.survey_ids

    async def _get_survey_details(self, survey_id: str) -> dict:
        """Get survey details"""
        survey_details = await self.client.get_survey_details(survey_id)
        survey_details = DetailsParser.parse_survey(survey_details)
        return survey_details

    async def _get_responses(self, survey_id: str, amount = 50, custom_variables: dict = None) -> list:
        """Get survey responses"""
        responses = await self.client.get_responses(survey_id, amount, custom_variables)
        responses = ResponseParser.parse_responses(responses)
        return responses

    # async def collect(self, amount = 50, custom_variables: dict = None) -> dict:
    #     """Collect survey details and responses"""
    #     details = aio.create_task(self.collect_details())
    #     responses = aio.create_task(self.collect_responses(amount, custom_variables))
    #     await details
    #     await responses
    #     details = details.result()
    #     responses = responses.result()
    #     return {
    #         survey_id: {
    #             "details": details[survey_id],
    #             "responses": responses[survey_id],
    #         }
    #         for survey_id in self.survey_ids
    #     }

    # async def collect_details(self) -> dict:
    #     """Collect survey details and responses"""
    #     survey_details = {survey_id: aio.create_task(self.get_survey_details(survey_id)) for survey_id in self.survey_ids}
    #     for survey_id, details in survey_details.items():
    #         await details
    #         survey_details[survey_id] = details.result()
    #     return survey_details

    # async def collect_responses(self, amount = 50, custom_variables: dict = None) -> dict:
    #     """Collect survey details and responses"""
    #     survey_responses = {survey_id: aio.create_task(self.get_responses(survey_id, amount, custom_variables)) for survey_id in self.survey_ids}
    #     for survey_id, response in survey_responses.items():
    #         await response
    #         survey_responses[survey_id] = response.result()
    #     return survey_responses
    
    async def create_df(self, survey_id: str, response_amount = 50, custom_variables: dict = None) -> pd.DataFrame:
        """Create a pandas dataframe from a survey"""
        details = self._get_survey_details(survey_id)
        responses = self._get_responses(survey_id, response_amount, custom_variables)
        details = await details
        responses = await responses
        return PandasParser(details, responses).convert()
    
    async def create_dfs(self, response_amount = 50, custom_variables: dict = None) -> dict:
        """Create pandas dataframes from surveys"""
        dfs: dict[str, aio.Task] = {}

        for survey_id in self.survey_ids:
            dfs[survey_id] = aio.create_task(self.create_df(survey_id, response_amount, custom_variables))
        
        for survey_id, df in dfs.items():
            await df
            dfs[survey_id] = df.result()
        
        return dfs
         

    def run(self, response_amount = 50, custom_variables: dict = None) -> pd.DataFrame:
        """Run the parser"""
        self.dfs = aio.run(self.create_dfs(response_amount, custom_variables))
        self._close()
    
        return self.dfs

    def _close(self) -> None:
        """Close the client session"""
        self.client.close()