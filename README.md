# Для кого проект? #
Для меня.
# Технологии #
Docker, Django, Python, Nginx
# Как развернуть проект #
Проект может быть развернут на локальном хосте и на удаленном сервере через контейнеры. Чтобы развернуть его на локальном хосте нужно запустить демон Docker и выполнить команды:
+ Запустить docker compose, чтобы взять контейнеры с открытого репозитория на докере:
```Bash
  docker compose -f docker-compose.production.yml up
```
+ Собрать статику:
```Bash
  docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
  docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/
```
+ Применить миграции:
```Bash
  docker compose -f docker-compose.production.yml exec backend python manage.py migrate
```
Чтобы развернуть:
```Bash
sudo docker compose -f docker-compose.production.yml up -d
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/
```
# Как заполнить env #
Перейти в .env файл и задать свои значения переменным:
Пример:
```
POSTGRES_USER=имя пользователя БД
POSTGRES_PASSWORD=пароль пользователя БД
POSTGRES_DB=название базы данных
DB_HOST=название базы данных хоста
DB_PORT=порт для базы данных
DEBUG=значение дебага
ALLOWED_HOSTS=допустимые хосты
```
