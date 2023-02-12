import aiohttp


class SurveyMonkey_API_Client:
    BASE_URL = "https://api.surveymonkey.net"

    SURVEY_ENDPOINT = "/v3/surveys"
    RESPONSES_ENDPOINT = lambda id: f"/v3/surveys/{id}/responses/bulk"

    def __init__(self, api_token: str):
        self.api_token = api_token
        self.session = aiohttp.ClientSession()

    async def _fetch(self, url: str, params: dict) -> dict:
        async with self.session.get(
            url, headers=self.generate_header(self.api_token), params=params
        ) as response:
            return await response.json()

    async def fetch_data(self, endpoint: str, params: dict) -> dict:
        data = await self._fetch(f"{self.BASE_URL}/{endpoint}", params=params)
        return data

    async def get_surveys(self, amount=50, search_str: str = "") -> list[dict]:
        response = await self.fetch_data(
            self.SURVEY_ENDPOINT, params={"per_page": amount, "title": search_str}
        )

        return response["data"]

    async def get_survey_by_id(self, id: str) -> list[dict]:
        response = await self.fetch_data(f"{self.SURVEY_ENDPOINT}/{id}")
        return response["data"]

    async def get_survey_details(self, id: str) -> dict:
        return await self.fetch_data(f"{self.SURVEY_ENDPOINT}/{id}/details")

    async def get_responses(
        self, id: str, amount: int = 50, custom_variables: dict = {}
    ) -> list[dict]:
        response = await self.fetch_data(
            self.RESPONSES_ENDPOINT(id),
            params={"per_page": amount, "custom_variables": custom_variables},
        )

        return response["data"]

    async def close(self):
        await self.session.close()

    @classmethod
    def generate_header(cls, api_token: str) -> dict:
        return {
            "Authorization": f"bearer {api_token}",
        }
