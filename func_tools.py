import dataclasses
from datetime import datetime

from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, \
    InlineKeyboardBuilder

from airtable_database import database, config

@dataclasses.dataclass
class MainMenuButtons:
    sign_up_to_train = "Записаться на тренировку"
    check_the_train = "Посмотреть запись о тренировках"
    show_all_the_trains = "Показать все тренировки на этой неделе"
    registration = "Заполнить информацию о себе"


def generate_registration_menu() -> "ReplyKeyboardMarkup":
    kb = [
        [KeyboardButton(text=MainMenuButtons.registration)]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    return keyboard


def generate_main_menu() -> "ReplyKeyboardMarkup":
    kb = [
        [KeyboardButton(text=MainMenuButtons.sign_up_to_train)],
        [KeyboardButton(text=MainMenuButtons.check_the_train)],
        [KeyboardButton(text=MainMenuButtons.show_all_the_trains)],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    return keyboard


def convert_date_to_locale(date):
    date = datetime.fromisoformat(date[:-1])
    date = date.replace(hour=date.hour + 3)  # добавляем 3 часа, чтобы скорректировать часовой пояс
    formatted_date = date.strftime('%d %B %Y г. %H:%M')
    return formatted_date


def generate_date_sport_inline_kb(train: str) -> "InlineKeyboardMarkup":

    sports = database.Sport(config.base_token, config.api_token)
    results = sports.get_sport_by_type(train)

    date_buttons = []
    for type_sport in results:
        date_buttons.append([InlineKeyboardButton(text=convert_date_to_locale(type_sport["fields"]["Дата проведения"]),
                                                  callback_data=type_sport["fields"]["Дата проведения"])])

    buttons = date_buttons
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def generate_types_sport_inline_kb() -> "InlineKeyboardMarkup":

    sports = database.Sport(config.base_token, config.api_token)
    results = sports.get_all_sports_unique()

    sport_buttons = []
    for every_sport in results:
        sport_buttons.append([InlineKeyboardButton(text=every_sport["fields"]["Тип спорта"], callback_data=every_sport["fields"]["Тип спорта"])])

    buttons = sport_buttons
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def generate_yes_no_kb() -> "InlineKeyboardMarkup":
    buttons = [
        [InlineKeyboardButton(text="Да", callback_data="yes")],
        [InlineKeyboardButton(text="Нет", callback_data="no")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard