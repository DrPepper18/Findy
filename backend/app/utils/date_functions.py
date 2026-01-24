from datetime import date
from dateutil.relativedelta import relativedelta

def calculate_age(born: date) -> int:
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def calculate_birthdate(age: int) -> date:
    today = date.today()
    birthdate = today - relativedelta(years=age)
    return birthdate.replace(month=1, day=1)