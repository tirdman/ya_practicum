FROM python:3.10

# Don't do this in a real project
ENV PG_HOST=db-dwh
ENV PG_USER=ya_practicum
ENV PG_PASSWORD=ya_practicum
ENV PG_DB=ya_practicum_db
ENV API_KEY=f072a563748ad70d73df526f6946841c

WORKDIR /usr/app/src

COPY get_currency.py .
COPY requirements.txt .

RUN pip3 install -r requirements.txt

CMD [ "python", "./get_currency.py"]
