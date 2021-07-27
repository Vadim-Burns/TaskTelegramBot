from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

months = [
    {
        "name": "January",
        "number": 1,
        "days": 31
    },
    {
        "name": "February",
        "number": 2,
        "days": 28
    },
    {
        "name": "March",
        "number": 3,
        "days": 31
    },
    {
        "name": "April",
        "number": 4,
        "days": 30
    },
    {
        "name": "May",
        "number": 5,
        "days": 31
    },
    {
        "name": "June",
        "number": 6,
        "days": 30
    },
    {
        "name": "July",
        "number": 7,
        "days": 31
    },
    {
        "name": "August",
        "number": 8,
        "days": 31
    },
    {
        "name": "September",
        "number": 9,
        "days": 30
    },
    {
        "name": "October",
        "number": 10,
        "days": 31
    },
    {
        "name": "November",
        "number": 11,
        "days": 30
    },
    {
        "name": "December",
        "number": 12,
        "days": 31
    },
]


def gen_years_markup(years: list) -> InlineKeyboardMarkup:
    """
    Example input:
    [2021, 2022, 2023]

    Example callback data:
    "year 2021"

    :param years: list of int

    :return: InlineKeyboardMarkup
    """
    markup = InlineKeyboardMarkup()

    for year in years:
        markup.add(
            InlineKeyboardButton(
                text=str(year),
                callback_data="year {year}".format(
                    year=year
                )
            )
        )

    return markup


def gen_months_markup(year: int) -> InlineKeyboardMarkup:
    """
    Example input:
    2021

    Example callback data:
    "month 2021 8"

    :param year: int of the chosen year

    :return: InlineKeyboardMarkup
    """
    markup = InlineKeyboardMarkup()

    for month in months:
        markup.add(
            InlineKeyboardButton(
                text=month.get("name"),
                callback_data="month {year} {month}".format(
                    year=year,
                    month=month.get("number")
                )
            )
        )

    return markup


def gen_days_markup(year: int, month: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    month = months[month - 1]
    days = month["days"]

    # Check for February
    if month["number"] == 2:
        if year % 4 == 0:
            days += 1

    # TODO: 2 days in one row
    for day in range(1, days + 1):
        markup.add(
            InlineKeyboardButton(
                text=str(day),
                callback_data="day {year} {month} {day}".format(
                    year=year,
                    month=month,
                    day=day
                )
            )
        )

    return markup
