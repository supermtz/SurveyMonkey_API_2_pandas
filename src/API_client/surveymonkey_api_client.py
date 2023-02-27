from enum import Enum
import json
import asyncio as aio
import aiohttp
# from asynci import as_completed

# class TokenAuthentication(Authbase):
#     """Attaches HTTPS API Token to a given Request object."""

#     def __init__(self, api_token: str):
#         self.api_token = api_token
    
#     def __call__(self, r: Request):
#         r.headers['Authentication'] = f"bearer {self.api_token}"

class Endpoint(str, Enum):
    SURVEY = "v3/surveys"
    RESPONSES = "v3/surveys/{id}/responses/bulk"


class SurveyMonkeyAPIClient:
    BASE_URL = "https://api.surveymonkey.net"

    def __init__(self, api_token: str):
        self.auth = {
            "Authorization": f"bearer {api_token}"
        }
        self.session: aiohttp.ClientSession = None
    
    # def __del__(self):
        # aio.run(self.session.close())
    
    async def get_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession(headers=self.auth)
        return self.session

    async def _fetch(self, url: str, params: dict) -> dict:
        async with aiohttp.ClientSession(headers=self.auth) as session:
            async with session.get(url, params=params) as response:
                return await response.json()
        session = await self.get_session()
        async with session.get(url, params=params) as response:
            return await response.json()

    async def fetch_data(self, endpoint: str, params: dict = {}) -> dict:
        data = await aio.create_task(self._fetch(f"{self.BASE_URL}/{endpoint}", params=params))
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
        if self.session:
            await self.session.close()
