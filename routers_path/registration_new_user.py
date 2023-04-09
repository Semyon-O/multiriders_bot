import pprint
from functools import partial

from aiogram import Router
import aiogram.filters as filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
import states as st

from airtable_database import database, config
import func_tools


router = Router()

saved_answers = {
    "phone": "",
    "name": "",
    "surname": "",
    "mail": ""
}


@router.message(filter.StateFilter(st.RegistrationStates.get_name))
async def get_name(message: Message, state: FSMContext):
    await message.answer(message.text)
    saved_answers["name"] = message.text
    await message.answer("Спасибо. Напишите пожалуйста вашу ФАМИЛИЮ:")
    await state.set_state(st.RegistrationStates.get_surname)


@router.message(filter.StateFilter(st.RegistrationStates.get_surname))
async def get_surname(message: Message, state: FSMContext):
    await message.answer(f"Ваша фамилия: {message.text}")
    saved_answers["surname"] = message.text
    await message.answer(f"Хорошо, напишите пожалуйста ваш телефон")
    await state.set_state(st.RegistrationStates.get_age)


@router.message(filter.StateFilter(st.RegistrationStates.get_age))
async def get_age(message: Message, state: FSMContext):
    await message.answer(f"Ваш телефон: {message.text}")
    saved_answers["phone"] = message.text
    await message.answer("Хорошо. По желанию, вы можете оставить свою почту, иначе поставьте '-'")
    await state.set_state(st.RegistrationStates.get_information)


async def _get_information(message: Message, state: FSMContext, saved_answers: dict):
    saved_answers["mail"] = message.text
    new_client = database.Client(config.base_token, config.api_token)
    new_client.create_client(message.from_user.id, saved_answers["phone"], saved_answers["name"],
                             saved_answers["surname"], saved_answers["mail"])


@router.message(filter.StateFilter(st.RegistrationStates.get_information))
async def get_information(message: Message, state: FSMContext):
    await partial(_get_information, saved_answers=saved_answers)(message, state)
    await message.answer("Спасибо за оставленные данные, нажмите /start чтобы начать заново.")

