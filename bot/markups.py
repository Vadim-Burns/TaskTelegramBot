from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove

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

# Yes/No markup is always the same, so we generate it only one time
yes_no_markup = ReplyKeyboardMarkup()

yes_no_markup.add(
    KeyboardButton(
        text="Yes"
    ),
    KeyboardButton(
        text="No"
    )
)

delete_markup = ReplyKeyboardRemove()


def gen_years_markup(years: list) -> InlineKeyboardMarkup:
    """
    Example input:
    [2021, 2022, 2023]

    Callback data format:
    year {year}

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

    Callback data format:
    month {year} {month}

    Example callback data:
    "month 2021 8"

    :param year: int of the chosen year

    :return: InlineKeyboardMarkup
    """
    markup = InlineKeyboardMarkup()

    for index in range(0, len(months), 2):
        if index + 1 < len(months):
            markup.add(
                InlineKeyboardButton(
                    text=months[index].get("name"),
                    callback_data="month {year} {month}".format(
                        year=year,
                        month=months[index].get("number")
                    )
                ),
                InlineKeyboardButton(
                    text=months[index + 1].get("name"),
                    callback_data="month {year} {month}".format(
                        year=year,
                        month=months[index + 1].get("number")
                    )
                )
            )
        else:
            markup.add(
                InlineKeyboardButton(
                    text=months[index].get("name"),
                    callback_data="month {year} {month}".format(
                        year=year,
                        month=months[index].get("number")
                    )
                )
            )

    return markup


def gen_days_markup(year: int, month: int) -> InlineKeyboardMarkup:
    """
    Example input:
    2021, 8

    Callback data format:
    day {year} {month} {day}

    Example callback data:
    "day 2021 8 14"

    :param year: int of the chosen year

    :param month: int of the chosen month

    :return: InlineKeyboardMarkup
    """
    markup = InlineKeyboardMarkup()
    month = months[month - 1]
    days = month.get("days")

    # Check for February
    if month.get("number") == 2:
        if year % 4 == 0:
            days += 1

    for day in range(1, days + 1, 2):
        if day + 1 <= days:
            markup.add(
                InlineKeyboardButton(
                    text=str(day),
                    callback_data="day {year} {month} {day}".format(
                        year=year,
                        month=month.get("number"),
                        day=day
                    )
                ),
                InlineKeyboardButton(
                    text=str(day + 1),
                    callback_data="day {year} {month} {day}".format(
                        year=year,
                        month=month.get("number"),
                        day=day + 1
                    )
                )
            )
        else:
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


def gen_hours_markup(year: int, month: int, day: int) -> InlineKeyboardMarkup:
    """
    Example input:
    2021, 8, 14

    Callback data format:
    day {year} {month} {day} {hour}

    Example callback data:
    "day 2021 8 14 19"

    :param year: int of the chosen year

    :param month: int of the chosen month

    :param day: int of the chosen day

    :return: InlineKeyboardMarkup
    """
    markup = InlineKeyboardMarkup()

    for hour in range(0, 24, 2):
        markup.add(
            InlineKeyboardButton(
                text=str(hour),
                callback_data="hour {year} {month} {day} {hour}".format(
                    year=year,
                    month=month,
                    day=day,
                    hour=hour
                )
            ),
            InlineKeyboardButton(
                text=str(hour + 1),
                callback_data="hour {year} {month} {day} {hour}".format(
                    year=year,
                    month=month,
                    day=day,
                    hour=hour + 1
                )
            )
        )

    return markup


def gen_minutes_markup(year: int, month: int, day: int, hour: int) -> InlineKeyboardMarkup:
    """
    Example input:
    2021, 8, 14, 19

    Callback data format:
    day {year} {month} {day} {hour} {minute}

    Example callback data:
    "day 2021 8 14 19 25"

    :param year: int of the chosen year

    :param month: int of the chosen month

    :param day: int of the chosen day

    :param hour: int of the chosen hour

    :return: InlineKeyboardMarkup
    """
    markup = InlineKeyboardMarkup()

    # Suggest every five minutes
    for minute in range(0, 60, 10):
        markup.add(
            InlineKeyboardButton(
                text=str(minute),
                callback_data="minute {year} {month} {day} {hour} {minute}".format(
                    year=year,
                    month=month,
                    day=day,
                    hour=hour,
                    minute=minute
                )
            ),
            InlineKeyboardButton(
                text=str(minute + 5),
                callback_data="minute {year} {month} {day} {hour} {minute}".format(
                    year=year,
                    month=month,
                    day=day,
                    hour=hour,
                    minute=minute + 5
                )
            )
        )

    return markup


def gen_yes_no_markup() -> ReplyKeyboardMarkup:
    """
    Returns simple markup with "Yes"/"No" answer

    :return: ReplyKeyboardMarkup
    """

    return yes_no_markup


def gen_delete_markup() -> ReplyKeyboardRemove:
    """
    Returns reply keyboard markup that cleans reply keyboard

    :return: ReplyKeyboardRemove
    """
    return delete_markup


def gen_delete_task_markup(task_id: int) -> InlineKeyboardMarkup:
    """
    Example input:
    14

    Callback data format:
    delete task {task_id}

    Example callback data:
    "delete task 14"

    Returns inline markup for deleting user task

    :param task_id: Id of the task to delete

    :return: InlineKeyboardMarkup
    """
    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton(
            text="Delete",
            callback_data="delete task {task_id}".format(task_id=task_id)
        )
    )

    return markup


def gen_delete_meeting_markup(meeting_id: int) -> InlineKeyboardMarkup:
    """
    Example input:
    14

    Callback data format:
    delete meeting {meeting_id}

    Example callback data:
    "delete meeting 14"

    Returns inline markup for deleting user meeting

    :param meeting_id: Id of the meeting to delete

    :return: InlineKeyboardMarkup
    """
    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton(
            text="Delete",
            callback_data="delete meeting {meeting_id}".format(meeting_id=meeting_id)
        )
    )

    return markup


def gen_edit_tasks_list_markup(tasks: 'list of Task') -> InlineKeyboardMarkup:
    """
    Example input:
    Task(name="My first task", description="some description", id=1)

    Callback data format:
    edit task start {task_id}

    Example callback data:
    "edit task start 1"

    Returns inline markup for the first step of edit task

    :param tasks: List of bot.database.Task

    :return: InlineKeyboardMarkup
    """
    markup = InlineKeyboardMarkup()

    for task in tasks:
        markup.add(
            InlineKeyboardButton(
                text=task.name.capitalize(),
                callback_data="edit task start {task_id}".format(task_id=task.id)
            )
        )

    return markup


def gen_edit_task_field_markup(task_id: int) -> InlineKeyboardMarkup:
    """
    Example input:
    14

    Callback data format:
    edit task {field} {task_id}

    Example callback data:
    "edit task name 14"

    Returns inline markup for the chosen field of edit task

    :param task_id: id of the task

    :return: InlineKeyboardMarkup
    """
    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton(
            text="Name",
            callback_data="edit task name {task_id}".format(task_id=task_id)
        )
    )

    markup.add(
        InlineKeyboardButton(
            text="Description",
            callback_data="edit task description {task_id}".format(task_id=task_id)
        )
    )

    markup.add(
        InlineKeyboardButton(
            text="Status",
            callback_data="edit task status {task_id}".format(task_id=task_id)
        )
    )

    return markup
