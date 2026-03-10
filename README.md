# Описание C#Study
Это увлекательное путешествие в мир в **C#**, где вы сможете изучить все аспекты языка и проверить свои знания.


## Используемый стек
* **Backend** - Python 3.11.14, FastAPI, SQLAlchemy(async), Alembic
* **Database** - PostgreSQL
* **Frontend** - Jinja, HTML5, CSS3
* **Auth** - JWT, PassLib

## Ключевые реализации
* **Безопасная авторизация** - через access и refresh токены.
  **Демонстрация формы регистрации**
  <img width="1468" height="784" alt="image" src="https://github.com/user-attachments/assets/5217e1c5-d216-40a3-90db-5f2ac8235a32" />
* **Панелья администратора** - вохможность удобно и безопасно работать с данными без прямого вмешательства в базу данных.
<img width="1468" height="784" alt="image" src="https://github.com/user-attachments/assets/80425a9b-9c7f-4e8e-a54e-dab3ae5b8f35" />
* **Динамический контент** - динамическая верстка HTML с помощью фильтров Jinja.
* **Последовательное обучение с закреплением знаний** - каждый небольшой блок теории содержит несколько тестовых заданий для освоения темы.
  **Пример теории**
  <img width="1468" height="784" alt="image" src="https://github.com/user-attachments/assets/40e0bc44-b610-40d9-b1c1-4bebcc52b278" />
  **Пример тестовых заданий с навигацией**
  <img width="1468" height="784" alt="image" src="https://github.com/user-attachments/assets/6c7eca14-bcb1-4f28-b3f1-50ad3fe8fe17" />

## Структура проекта
Каждая структура отвечает **ТОЛЬКО** за эту структура
Модули в каждой структуре:
* *struct*/dao - для работы с запросами к базе данных
* *struct*/models - для проведения миграций
* *struct*/router - для реализации бизнес логики в endpoint
* *struct*/schemas - для валидации данных через Pydantic
* *struct*/dependenies - для вызова связанных функций. Сделан с целью декомпозиции
* *struct*/auth - для работы с JWT токенами
