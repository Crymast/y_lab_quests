Подготовка проекта
---
---

![Typing SVG](https://readme-typing-svg.herokuapp.com?color=%13385&lines=Виртуальное+окружение)

Создание виртуального окружения:

`python -m venv venv`

Активация виртуального окружения

`venv\Scripts\activate.bat`

---

Установка необходимых библиотек:

`pip install -r requirements.txt`

Запуск приложения:

`uvicorn main:app --reload`

---

Создание баз, запустить последовательно:

`alembic revision --autogenerate -m "Database init"`

Номер в конце подставить из сформированного файла в
[migration/versions](migration%2Fversions)

`alembic upgrade head`

---

По завершению написать example.env с комментариями

---
