from aiogram import Router
from aiogram.filters import Text
from aiogram.types import Message
import func_tools as ft

router = Router()


@router.message(Text(ft.MainMenuButtons.check_the_train))
async def get_signed_trains(message: Message):
    ...