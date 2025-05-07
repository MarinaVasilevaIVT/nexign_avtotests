import pytest
import json
import datetime
import requests
from cdr.avto_generate_cdr import generate_phone_number

BASE_URL = "http://example.com"


def create_cdr_record(call_type, msisdn, called, start_time, end_time):
    return {
        "call_type": call_type,
        "caller": msisdn,
        "called": called,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat()
    }

def post_cdr_to_brt(cdr):
    url = f"{BASE_URL}/cdr"
    response = requests.post(url, json=cdr)
    assert response.status_code == 200

def get_brt_balance(msisdn):
    response = requests.get(f"{BASE_URL}/balance/{msisdn}")
    assert response.status_code == 200
    return response.json()["balance"]

def get_last_debit_json(msisdn):
    response = requests.get(f"{BASE_URL}/last-debit/{msisdn}")
    assert response.status_code == 200
    return response.json()

@pytest.fixture
def classic_subscriber():
    # Фикстура для создания абонента с тарифом "Классика"
    msisdn = "79684597864"
    subscriber_data = {
        "msisdn": msisdn,
        "tariffId": 11
    }
    response = requests.post(f"{BASE_URL}/save", json=subscriber_data)
    assert response.status_code == 200
    return msisdn


def test_classic_call_under_one_minute(classic_subscriber):
    """
    Проверка списания за звонок меньше минуты.
    Ожидаем округление до 1 минуты и списание 1.5 у.е. (внутрисетевой звонок).
    """
    msisdn = classic_subscriber
    start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(seconds=45)

    cdr = create_cdr_record('01', msisdn, generate_phone_number(), start_time, end_time)
    post_cdr_to_brt(cdr)

    debit_json = get_last_debit_json(msisdn)
    assert debit_json["Phone_number"] == msisdn
    assert debit_json["ID_tariff"] == "11"
    assert debit_json["Debit"] == pytest.approx(1.5)


def test_classic_call_over_six_minutes_external(classic_subscriber):
    """
    Проверка списания за звонок продолжительностью более 6 минут (внешний).
    Должно быть округлено до 7 минут, тариф 2.5 => 17.5 у.е.
    """
    msisdn = classic_subscriber
    start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(minutes=6, seconds=22)

    cdr = create_cdr_record('01', msisdn, generate_phone_number(), start_time, end_time)
    post_cdr_to_brt(cdr)

    debit_json = get_last_debit_json(msisdn)
    assert debit_json["Phone_number"] == msisdn
    assert debit_json["ID_tariff"] == "11"
    assert debit_json["Debit"] == pytest.approx(17.5)
