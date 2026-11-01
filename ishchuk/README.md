# Облік завдань

Лабораторна робота №6–7. Іщук Павло Олегович, КІ-31.

Flask + SQLite, окремий DAL, таблиця з шістьма стовпцями, повний CRUD.

```sh
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

У Linux: `source venv/bin/activate`. Відкрити http://127.0.0.1:5058/.
База `data.db` створюється автоматично поруч із app.py і не входить у Git.

Перевірка: `python -m unittest -v`. Тести використовують окрему тимчасову БД.

Маршрути: GET `/`, GET/POST `/add`, GET/POST `/edit/<id>`, POST `/delete/<id>`.
Запити параметризовані, форми перевіряють CSRF-токен, HTML екранує введений текст.
Це навчальний однокористувацький застосунок для локального запуску; автентифікацію не реалізовано.
