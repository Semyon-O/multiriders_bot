from aiogram import Router
import aiogram.filters as filter
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
import states as st
import func_tools as ft

from airtable_database import database, config

router = Router()

saved_answers = {
    "type_train": "",
    "date": ""
}


@router.callback_query(filter.StateFilter(st.MakingRecordToTrain.choosing_type_sport))
async def choose_train(callback: CallbackQuery, state: FSMContext):
    saved_answers["type_train"] = callback.data
    await callback.message.answer(f"Вы выбрали {callback.data}"
                                  f"\nВыберите даты проведения тренировки", reply_markup=ft.generate_date_sport_inline_kb(callback.data))

    global all_typed_trains
    all_typed_trains = database.Sport(config.base_token, config.api_token).get_sport_by_type(saved_answers["type_train"])

    await state.set_state(st.MakingRecordToTrain.choosing_date)


@router.callback_query(filter.StateFilter(st.MakingRecordToTrain.choosing_date))
async def choose_date(callback: CallbackQuery, state: FSMContext):
    saved_answers["date"] = callback.data
    await callback.message.answer(f"Вы выбрали дату проведения: {callback.data}")

    new_record = database.Record(config.base_token, config.api_token)
    client = database.Client(config.base_token, config.api_token)
    id_client = client.get_client_by_id_user(callback.from_user.id)

    matching_records = []

    for record in all_typed_trains:
        if record["fields"]["Дата проведения"] == saved_answers["date"]:
            matching_records.append(record)

    print(matching_records)
    new_record.create_record([matching_records[0]["id"]], [id_client[0]["id"]])
    await callback.message.answer("Спасибо, мы сохранили вашу заявку.")


#
# @router.message(filter.StateFilter())
# async def confirm(message: Message, state: FSMContext):
#     ...




