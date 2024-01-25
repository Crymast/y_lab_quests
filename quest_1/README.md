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

---

Создание баз, запустить последовательно:

Создать каталог
[migration/versions](migration%2Fversions)

`alembic revision --autogenerate -m "Database init"`

[migration/versions](migration%2Fversions)

`alembic upgrade head`

---

По завершению написать example.env с комментариями

---