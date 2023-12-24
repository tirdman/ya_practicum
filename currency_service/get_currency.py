import os
from urllib.request import urlopen
import json
from typing import NamedTuple
from datetime import datetime
from decimal import Decimal
import psycopg2 as pg

API_URL = 'http://api.exchangerate.host/live?access_key={access_key}&currencies={currency_pair}'
CURRENCY_PAIR = os.getenv('CURRENCY_PAIR', "USD,RUB")

PG_HOST = os.getenv('PG_HOST')
PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_DB = os.getenv('PG_DB')
API_KEY = os.getenv('API_KEY')


class CurrencyInfo(NamedTuple):
    exchange_dt: datetime
    currency_pair: str
    rate: Decimal


class ApiRequestParam(NamedTuple):
    exchange_dt: datetime | None
    currency_pair: str


def get_currency(params: ApiRequestParam) -> CurrencyInfo:
    """
    Получение данных курса валют
    :param params: Параметр для запроса
    :return: Данные курса
    """
    uri = API_URL.format(access_key=API_KEY, currency_pair=params.currency_pair)
    with urlopen(uri) as response:
        _data = json.load(response)

        return CurrencyInfo(
            exchange_dt=datetime.utcfromtimestamp(_data["timestamp"]),
            currency_pair=CURRENCY_PAIR.replace(',', ''),
            rate=_data["quotes"][CURRENCY_PAIR.replace(',', '')],
        )


if __name__ == '__main__':
    """
    Для простоты нет проверок и вызова кастомных исключений
    """

    param = ApiRequestParam(
        exchange_dt=None,
        currency_pair=CURRENCY_PAIR
    )

    data = get_currency(param)
    conn = pg.connect(f"dbname={PG_DB} user={PG_USER} password={PG_PASSWORD} host={PG_HOST}")
    with conn as tx:
        with tx.cursor() as curs:
            curs.execute(
                'INSERT INTO sandbox.exchange_rate (exchange_dt, currency_pair, rate) VALUES (%s, %s, %s)',
                (data.exchange_dt, data.currency_pair, data.rate))
