# api_yamdb

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/AlexanderKhasanov/api_yamdb
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Script/activate
```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```
