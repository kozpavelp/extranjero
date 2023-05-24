from aiogram import Router
from aiogram.filters import Text
from aiogram.types import Message

from lexicon.lexicon import LEXICON
from services.parser import soldol


router: Router = Router()


@router.message(Text(text=['курс', 'Курс']))
async def course(message: Message):
    amount = soldol()
    await message.answer(text=f"{LEXICON['sol']} {amount}")
