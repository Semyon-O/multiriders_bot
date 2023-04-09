from aiogram.fsm.state import StatesGroup, State


class MakingRecordToTrain(StatesGroup):
    choosing_type_sport = State()
    choosing_date = State()
    confirm_data = State()


class RegistrationStates(StatesGroup):
    get_nickname = State()
    get_name = State()
    get_surname = State()
    get_age = State()
    get_information = State()

