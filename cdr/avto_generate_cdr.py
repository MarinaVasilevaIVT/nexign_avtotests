import random
import datetime
from datetime import timedelta, datetime
import csv

def generate_phone_number():
    """Генерация случайного номера телефона в формате 79XXXXXXXXX"""
    return f"79{random.randint(000000000, 999999999)}"

def generate_random_datetime(start_year=2023, end_year=2025):
    """Генерация случайной даты и времени в пределах заданного диапазона"""
    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)
    if month == 2:
        day = random.randint(1, 28)
    elif month in [1, 3, 5, 7, 8, 10, 12]:
        day = random.randint(1, 31)
    else:
        day = random.randint(1, 30)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    dt_str = "2009-05-28T16:15:00"
    return datetime(year, month, day, hour, minute, second)

def generate_call_duration():
    return timedelta (seconds=random.randint(1, 86399)) #выбрала для максимальной длительности звонка 23:59:59

def split_call_over_midnight(start_time, finish_time):
    midnight = datetime(start_time.year, start_time.month, start_time.day) + timedelta(days=1)
    
    if finish_time > midnight:
        # Первая часть (до полуночи)
        first_part_end = midnight - timedelta(seconds=1)
        first_record = (start_time, first_part_end)
        
        # Вторая часть (после полуночи)
        second_record = (midnight, finish_time)
        
        return [first_record, second_record]
    else:
        return [(start_time, finish_time)]


def generate_positive_cdr(num_records=10):
    """Генерация валидной CDR записи"""

    cdr_records = []

    while len(cdr_records) < num_records:

        call_type = random.choice(["01", "02"])
        
        # Генерация уникальных номеров
        phone_caller = generate_phone_number()
        phone_called = generate_phone_number()
        while phone_called == phone_caller:
            phone_called = generate_phone_number()
        
        start_time = generate_random_datetime()
        duration = generate_call_duration()
        finish_time = start_time + duration

        # Если звонок переходит через полночь, разбиваем его на две записи
        call_parts = split_call_over_midnight(start_time, finish_time)

        for part_start, part_finish in call_parts:
            record = f"{call_type},{phone_caller},{phone_called},{part_start.isoformat()},{part_finish.isoformat()}"
            cdr_records.append(record)

             # Если уже набрали нужное количество записей, выходим
            if len(cdr_records) >= num_records:
                break
    
    # Сортируем записи по времени начала звонка
    cdr_records = sorted(cdr_records, key=lambda x: x.split(',')[3])

    return "\n".join(cdr_records[:num_records])  # Возвращаем ровно num_records записей
        
def generate_negative_cdr(case_type, num_records=10):
    """Генерация невалидной CDR записи"""

    cdr_records = []

    while len(cdr_records) < num_records:

        call_type = random.choice(["01", "02"])
        
        phone_caller = generate_phone_number()
        phone_called = generate_phone_number()
        while phone_called == phone_caller:
            phone_called = generate_phone_number()
        
        start_time = generate_random_datetime()
        duration = generate_call_duration()
        finish_time = start_time + duration

        call_parts = split_call_over_midnight(start_time, finish_time)  
        
        # Модификация для негативных тестов
        if case_type == "invalid_type_of_call":
            call_type = random.choice(["03", "04", "05"])
        
        elif case_type == "invalid_operator_called":
            # Несуществующий оператор (не начинается с 79) для абонента, с которым осуществлялась связь
            phone_called = f"{random.choice([0,1,2,3,4,5,6,8,9])}{random.randint(0000000000, 9999999999)}"
        
        elif case_type == "invalid_number_called":
            # Некорректный номер (неправильная длина) для абонента, с которым осуществлялась связь
            phone_called = f"79{random.randint(100000, 999999)}"  # Слишком короткий
        
        elif case_type == "invalid_operator_caller":
            # Несуществующий оператор (не начинается с 79) для обслуживаемого абонента
            phone_caller = f"{random.choice([0,1,2,3,4,5,6,8,9])}{random.randint(0000000000, 9999999999)}"
        
        elif case_type == "invalid_number_caller":
            # Некорректный номер (неправильная длина) для обслуживаемого абонента
            phone_caller = f"79{random.randint(100000, 999999)}"  # Слишком короткий
        
        elif case_type == "long_duration":
            # Длительность больше 24 часов
            duration = timedelta(days=1, seconds=random.randint(1, 86400))
            finish_time = start_time + duration
        
        elif case_type == "wrong_order":
            # Время окончания раньше времени начала
            finish_time, start_time = start_time, finish_time

        elif case_type == "invalid_date":
            # Некорректная дата начала/окончания
            if random.choice([True, False]):
                start_time = "2025-13-32T25:61:61"  # Некорректная дата
            else:
                finish_time = "2025-00-00T00:00:00"  # Некорректная дата
        
        record = f"{call_type},{phone_caller},{phone_called},{start_time},{finish_time}"
        cdr_records.append(record)
    
    cdr_records = sorted(cdr_records, key=lambda x: x.split(',')[3])
    
    return "\n".join(cdr_records)


def save_to_file(content, filename):
    with open(filename, 'w') as f:
        f.write(content)

# Пример использования:
if __name__ == "__main__":
    # Генерация позитивного CDR
    positive_cdr = generate_positive_cdr()
    save_to_file(positive_cdr, "positive_test.csv")
    
    # Генерация негативных CDR
    negative_cases = [
        "invalid_type_of_call", #Некорректный тип звонка
        "invalid_date",     # Некорректная дата
        "invalid_operator_caller",  # Несуществующий оператор обслуживаемого абонента
        "invalid_number_caller",    # Некорректный номер обслуживаемого абонента
        "invalid_operator_called",  # Несуществующий оператор абонента, с которым осуществлялась связь
        "invalid_number_called",    # Некорректный номер абонента, с которым осуществлялась связь
        "long_duration",    # Длительность >24h
        "wrong_order"       # Время окончания раньше начала
    ]
    
    negative_cdr_format = generate_positive_cdr()
    #сохранение не в корректном формате
    save_to_file(negative_cdr_format, "negative_cdr.doc")

    for i, case in enumerate(negative_cases, 1):
        negative_cdr = generate_negative_cdr(case)
        save_to_file(negative_cdr, f"negative_test_{i}.csv")