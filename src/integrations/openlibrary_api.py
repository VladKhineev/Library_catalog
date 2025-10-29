import httpx
from src.models.book_model import BookExternalInfo

class OpenLibraryAPI:
    BASE_URL = "https://openlibrary.org/search.json"

    def fetch_book_info(self, title: str) -> BookExternalInfo:
        response = httpx.get(self.BASE_URL, params={'title': title})
        data = response.json()

        if not data['docs']:
            return BookExternalInfo()

        book = data['docs'][0]

        return BookExternalInfo(
            cover=f'https://covers.openlibrary.org/b/id/{book.get('cover_i')}-L.jpg' if book.get('cover_i') else None,
            description=book.get('first_sentence', {}).get('value'),
        )