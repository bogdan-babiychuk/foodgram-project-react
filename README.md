# Foodgrams - Cервис для создания и просмотра рецептов.

### Возможности сервиса:
FoodGram - это онлайн-сервис для создания, просмотра, добавления в избранное и создания списка покупок рецептов.
Вы также можете подписываться на других авторов и делиться своими рецептами.

### Установка:
1. Клонируйте проект:
    ```bash
    git clone https://github.com/babiychukbogdan/foodgram-project-react.git
    ```
    ```bash
    cd foodgram-project-react
    ```
2. Собираем контейнеры и делаем миграции:
```
sudo docker compose up -d
sudo docker-compose exec backend python manage.py migrate
```
3. Cобериаем статику:
```
sudo docker-compose exec backend python manage.py collectstatic
sudo docker compose exec backend cp -r /app/collected_static/. /backend_static/static/
```
4. Супер юзер:
```
email: test@mail.ru
password: 243245
```
### Сервис доступен по домену:
```
https://foodgrams.ddnsking.com
```

## Автор
Бабийчук Богдан
