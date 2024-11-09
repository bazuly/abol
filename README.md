Image Processing API - это Django REST API для обработки изображений с использованием RabbitMQ для обработки событий.
Приложение предоставляет функции для загрузки изображений, их обработки и преобразования в различные размеры, а также JWT-аутентификацию для безопасного доступа к API.


Основные функции

- Загрузка изображений и их обработка (уменьшение, изменение формата и т.п.)
- JWT-аутентификация пользователей с использованием rest_framework_simplejwt
- Поддержка асинхронной обработки событий через RabbitMQ
- Документация API через Swagger (drf_yasg)

Стек технологий

    Backend: Django, Django REST framework
    Broker: RabbitMQ
    Database: PostgreSQL
    API Documentation: Swagger через drf_yasg

Установка и требования к запуску

    Docker и Docker Compose
    Python 3.12 или выше (для локальной разработки)

Шаги для установки:

    git clone git@github.com:bazuly/abol.git
    cd abol

Создайте файл .env в корневой директории проекта и добавьте необходимые переменные окружения. Пример:

    POSTGRES_DB=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_HOST=db
    POSTGRES_PORT=5432

Собираем контейнер.

    docker-compose up --build -d 
    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py createsuperuser

Также мы можем воспользоваться утилитой make, я написал тестовый Makefile.

    Данная утилита предназначена для упрощенного ввода команд в терминал,
    например: make app, которая равна docker-compose up --build -d
    К сожалению данная утилита работает корректно только на Линуксе,
    поэтому я не стал акцентировать на ней внимание, т.к. большинство скорее всего работает под windows.
    Но шаблонный Makefile все равно оставлю в репозитории, можете ознакомиться, если интересно.
    P.S Через wsl тоже работает, через Ubuntu, например.

Доступ к приложению

    API: http://localhost:8000/
    Документация Swagger: http://localhost:8000/api/swagger/
    Панель администратора Django: http://localhost:8000/admin/

Все загруженные изображения сохраняется по дефолтным настройкам Django в папке media.
Обработанные изображения сохраняется в директории media_converted внутри основного проекта. 

В качестве архитектуры был выбран практически дефолтный django, с некоторыми кастомными изменениями. 
В качестве улучшений можно добавить абсолютный путь к apps, в sys.path, это на мой взгляд может упростить настройки приложений и работу с docker. 
Ниже приведён пример исполнения:
![изображение](https://github.com/user-attachments/assets/487be877-b69f-4d14-afef-0b9e5093c364)


В больших проектах, я считаю, что нужно использовать уже готовые решения, сам пользуюсь django-cookiecutter.
Или же можете ознакомиться с моей версией django-boilerplate https://github.com/bazuly/django-docker-compose-postgres-boilerplate. 
