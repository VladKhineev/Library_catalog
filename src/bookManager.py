import src.safeData as safeData
import src.models as models


class BookManager:
    def __init__(self):
        self.repo = safeData.JSONRepository('data.json')



bm = BookManager()
book = models.Book(**{
  "id": 4,
  "title": "string",
  "autor": "string",
  "year": 1220,
  "genre": "string",
  "count_page": 0,
  "accessibility": "в наличии"
})

