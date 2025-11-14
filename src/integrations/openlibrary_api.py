import httpx

from src.integrations.base_api_client import BaseApiClient
from src.api.schemas.book import BookExternalInfo


class OpenLibraryAPI(BaseApiClient):
    BASE_URL = "https://openlibrary.org/search.json"
    WORKS_URL = "https://openlibrary.org"

    async def fetch_book_info(self, title: str) -> BookExternalInfo:
        async with httpx.AsyncClient() as client:
            response = await client.get(self.BASE_URL, params={'title': title})
            data = response.json()

            if not data['docs']:
                return BookExternalInfo()

            book = data['docs'][0]

            cover_id = book.get('cover_i')
            cover_url = (
                f'https://covers.openlibrary.org/b/id/{cover_id}-L.jpg'
                if cover_id
                else None
            )

            # по ключу книги достаём описание
            work_key = book.get('key')
            description = None

            if work_key:
                work_url = f"{self.WORKS_URL}{work_key}.json"
                work_response = await client.get(work_url)
                if work_response.status_code == 200:
                    work_data = work_response.json()
                    desc = work_data.get("description")
                    if isinstance(desc, dict):
                        description = desc.get("value")
                    elif isinstance(desc, str):
                        description = desc

        return BookExternalInfo(cover=cover_url, description=description)


if __name__ == '__main__':
    api = OpenLibraryAPI()
    print(api.fetch_book_info(title='The Hobbit'))
