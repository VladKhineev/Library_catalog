import json
import os
from pydantic import BaseModel

import src.models as models


class JSONRepository:
    def __init__(self, filename: str):
        self.filename = filename

    def save_data(self, data: dict):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([data], file, ensure_ascii=False, indent=4)

    def load_data(self) -> list:
        with open(self.filename, 'r', encoding='utf-8') as file:
            data: list = json.load(file)
        return data



        # # Загружаем старые данные (если есть)
        # if os.path.exists(self.filename):
        #     with open(self.filename, "r", encoding="utf-8") as f:
        #         try:
        #             data = json.load(f)
        #         except json.JSONDecodeError:
        #             data = []
        # else:
        #     data = []
        #
        # # 2. Добавляем новые данные
        # data.append(item.model_dump())
        #
        # # 3. Сохраняем обратно
        # with open(self.filename, "w", encoding="utf-8") as file:
        #     json.dump(data, file, ensure_ascii=False, indent=4)

j = JSONRepository('book.json')
data = {
    'name': 'Dima',
    'id': 2,
}

j.save_data(data)
print(j.load_data())