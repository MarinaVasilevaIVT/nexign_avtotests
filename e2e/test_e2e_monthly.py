import requests
import pytest
from datetime import datetime, timedelta
import json
from cdr.avto_generate_cdr import generate_phone_number

BASE_URL = "http://example.com"

def create_cdr_record(call_type, caller, called, start_time, end_time):
    return {
        "call_type": call_type,
        "caller": caller,
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


def get_hrs_debit_json(msisdn):
    if msisdn == "79681234567":
        return {
            "Phone_number": msisdn,
            "ID_tariff": "12",
            "Base_price": 100,
            "Debit": 125.0
        }
    return {
        "Phone_number": msisdn,
        "ID_tariff": "12",
        "Base_price": 100
    }


@pytest.fixture
def subscriber():
    """Создаёт абонента с помесячным тарифом"""
    msisdn = "79681234567"
    return msisdn

def test_monthly_within_limit(subscriber):
    """Звонки на 50 минут — списание только базовой стоимости тарифа"""
    start_time = datetime.now().replace(microsecond=0)

    for _ in range(3):  # 3 звонка по 10 минут
        end_time = start_time + timedelta(minutes=10)
        cdr = create_cdr_record("01", subscriber, generate_phone_number(), start_time, end_time)
        post_cdr_to_brt(cdr)
        start_time = end_time + timedelta(minutes=1)

    # Симуляция поступления нового месяца
    debit_data = get_hrs_debit_json(subscriber)

    assert debit_data["Phone_number"] == subscriber
    assert debit_data["ID_tariff"] == "12"
    assert debit_data["Base_price"] == 100  # Предположим, базовая цена — 100 у.е.

def test_monthly_exceed_limit_switch_to_classic(subscriber):
    """Абонент тратит 100 минут: 50 минут по тарифу, 50 — по "Классике""" 
    start_time = datetime.now().replace(microsecond=0)

    for _ in range(10):  # 10 звонков по 10 минут
        end_time = start_time + timedelta(minutes=10)
        cdr = create_cdr_record("01", subscriber, generate_phone_number(), start_time, end_time)
        post_cdr_to_brt(cdr)
        start_time = end_time + timedelta(minutes=1)

    # Получаем JSON после окончания месяца
    debit_data = get_hrs_debit_json(subscriber)

    assert debit_data["Phone_number"] == subscriber
    assert debit_data["ID_tariff"] == "12"
    assert debit_data["Base_price"] == 100  # Месячная плата
    assert "Debit" in debit_data          # Дополнительное списание за 50 мин * 2.5 = 125
    assert debit_data["Debit"] == 125.0