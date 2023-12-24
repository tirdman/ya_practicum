Задание 3 

Используя API [exchangerate.host](https://exchangerate.host/), подготовьте ETL процесс с помощью Airflow на Python для выгрузки данных по валютной паре BTC/USD (Биткоин к доллару). 
Выгружать следует с шагом 3 часа и записывать данные в БД (валютная пара, дата, текущий курс).
В качестве задания со звёздочкой можете учесть вариант заполнения базы историческими данными (API предоставляет специальный endpoint для выгрузки исторических данных).

## Инструкция запуска решения

1) Склонировать проект на локальный компьютер и перейти в каталог
```
git clone https://github.com/tirdman/ya_practicum.git && cd ya_practicum/task_3
```

2) Создать сервис

Перейти в директорию currency_service
```
cd currency_service
```
Создать docker-образ сервиса
```
docker build . -t currency_rate
```

3) Создание компонентов Airflow и базы данных выгрузки результатов

Перейти в директорию airflow_and_db
```
cd ../airflow_and_db
```


Создать контейнеры:
- Компоненты AIrflow 
- docker-proxy для запуска контейнера из докер-контейнера локально 
- Отдельный инстанс Postgres для сохранения результатов (должен быть отдельно, но для простоты так)
```
docker-compose up -d 
```

Запуск миграции подготовки объектов db для дальнейшего сохранения результатов
```
docker exec -u postgres airflow_and_db-db-dwh-1 psql -U postgres -f /migration.sql
```

Заполнение истории
```
docker exec airflow_and_db-airflow-worker-1 airflow dags backfill currency_service_daily_1 -s 2023-12-20 -e 2023-12-23
```

