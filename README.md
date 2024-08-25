# Task Management BackEnd

## project setup

1

```
cd Task_Management
```

2- SetUp venv

```
virtualenv -p python3.10 venv
source venv/bin/activate
```

3- install Dependencies

```
pip install -r requirements.txt
```

4- create your env

```
cp .env.dev .env
```

5- Create tables

```
python manage.py migrate
```

6- spin off docker compose

```
docker compose -f compose.dev.yml up -d
```

7- run the project

```
python manage.py runserver
```
