from enum import Enum
import json
import aiohttp


class Endpoint(str, Enum):
    SURVEY = "v3/surveys"
    RESPONSES = "v3/surveys/{id}/responses/bulk"


class SurveyMonkeyAPIClient:
    BASE_URL = "https://api.surveymonkey.net"

    def __init__(self, api_token: str):
        self.api_token = api_token
        self.session = aiohttp.ClientSession()

    async def _fetch(self, url: str, params: dict) -> dict:
        async with self.session.get(
            url, headers=self.generate_header(self.api_token), params=params
        ) as response:
            return await response.json()

    async def fetch_data(self, endpoint: str, params: dict = {}) -> dict:
        data = await self._fetch(f"{self.BASE_URL}/{endpoint}", params=params)
        return data

    async def get_surveys(self, amount=50, search_str: str = None) -> list[dict]:
        params = {"per_page": amount}

        if search_str:
            params["title"] = search_str

        response = await self.fetch_data(Endpoint.SURVEY, params=params)

        return response["data"]

    async def get_survey_by_id(self, id: str) -> list[dict]:
        response = await self.fetch_data(f"{Endpoint.SURVEY}/{id}")
        return response["data"]

    async def get_survey_details(self, id: str) -> dict:
        return await self.fetch_data(f"{Endpoint.SURVEY}/{id}/details")

    async def get_responses(
        self, id: str, amount: int = 50, custom_variables: dict = None
    ) -> list[dict]:
        params = {"per_page": amount}

        if custom_variables:
            params["custom_variables"] = json.dumps(custom_variables, indent=None)

        response = await self.fetch_data(
            Endpoint.RESPONSES.format(id=id),
            params=params,
        )

        return response["data"]

    async def close(self):
        await self.session.close()

    @classmethod
    def generate_header(cls, api_token: str) -> dict:
        return {
            "Authorization": f"bearer {api_token}",
        }
