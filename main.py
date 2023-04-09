import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
import aiogram.filters as filter
from aiogram.fsm.storage.memory import MemoryStorage

import states as st
import func_tools
from routers_path import sign_up_to_train, registration_new_user

from airtable_database import config, database

logging.basicConfig(level=logging.INFO)
bot = Bot(token="5912451942:AAG2gF8ShXvIeY90On-0f687xQZWZTpckNU")
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(sign_up_to_train.router)
dp.include_router(registration_new_user.router)


# TODO: Сделать просмотр заявок
# TODO: Сделать функ. удаления
# TODO: Функ. редактирования
# TODO: найти CRM (Notion, Google Sheets) или сделать бота администратора


@dp.message(filter.Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):

    entered_client = database.Client(config.base_token, config.api_token)

    user_id = message.from_user.id
    print(entered_client.get_client_by_id_user(user_id))
    if entered_client.get_client_by_id_user(user_id) != []:
        await message.answer(f"👋 Здравствуйте. Вы зашли как {message.from_user.username}", reply_markup=func_tools.generate_main_menu())

    else:
        await message.answer("Приветсвуем в чат-боте по воскресным тренировкам. Заполните немного о себе, чтобы в будущем "
                         "быстрее создавать заявки")
        await message.answer("Напишите пожалуйста ваше ИМЯ:")
        await state.set_state(st.RegistrationStates.get_name)


@dp.message(filter.Text(func_tools.MainMenuButtons.sign_up_to_train))
async def sign_up_to_train(message: types.Message, state: FSMContext):
    await message.answer("Отлично, для записи, мы будем использовать те данные, "
                         "которые вы оставили при регистрации в этот бот.")
    await message.answer("Выберите интересующий вас тип спорта ⛷:", reply_markup=func_tools.generate_types_sport_inline_kb())
    await state.set_state(st.MakingRecordToTrain.choosing_type_sport)


@dp.message(filter.Text(func_tools.MainMenuButtons.check_the_train))
async def show_signed_trains(message: types.Message, state: FSMContext):
    await message.answer("Здесь отображаются ваши заявки, которые вы оставляли ранее.")
    user_id = message.from_user.id
    records = database.Record(config.base_token, config.api_token).get_records_by_client_id(user_id)
    for every_record in records:
        await message.answer(
            f"""\n<b>Ваш номер заявки</b> №: {every_record["fields"]["Номер заявки"].__str__()}"""
            f"""\n⛷ <b>Тип спорта</b> ⛷: {every_record["fields"]["Тип спорта (from Тип спорта)"].__str__()}"""
            f"""\n📅 <b>Дата проведения</b> 📅: {every_record["fields"]["Дата проведения"]}""", parse_mode="HTML")


@dp.message(filter.Text(func_tools.MainMenuButtons.show_all_the_trains))
async def show_all_trains(message: types.Message, state: FSMContext):
    await message.answer("Функция сейчас недоступна")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())