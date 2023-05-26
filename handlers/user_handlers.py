import os
from aiogram import Router, F, Bot
from aiogram.filters import Text
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


from lexicon.lexicon import LEXICON
from services.parser import soldol
from services.voice import voice_to_text, save_mp3
from services.deleter import temp_del


router: Router = Router()


@router.message(Text(text=['курс', 'Курс']))
async def course(message: Message):
    amount = soldol()
    await message.answer(text=f"{LEXICON['sol']} {amount}")


@router.message(F.voice)
async def voice_detected(message: Message, bot: Bot):
    voice_path = await save_mp3(bot, message.voice)
    await temp_del()
    yes_btn = InlineKeyboardButton(text=LEXICON['yes'], callback_data=f'yes:{voice_path}')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[yes_btn]])

    await message.answer(text='Перевести голос в текст?', reply_markup=keyboard)

@router.callback_query(lambda callback: callback.data.startswith('yes:'))
async def voice_transcript(callback: CallbackQuery):
    voice_path = callback.data.split(':')[1]
    transcripted = await voice_to_text(voice_path)
    if os.path.exists(voice_path):
        os.remove(voice_path)
    if transcripted:
        await callback.message.edit_text(text=transcripted)
