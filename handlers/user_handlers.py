import os
from copy import deepcopy
from aiogram import Router, F, Bot
from aiogram.filters import Text
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database.dict_db import user_db, user_dict_template
from lexicon.lexicon import LEXICON
from services.result_func import main_func
from services.currency_parsers import soldol
from services.voice import voice_to_text, save_mp3
from services.deleter import temp_del
from keyboards.keyboards import (city_choice, source_choice, pagination_kb,
                                 begin_or_archive, bookmark_choice, bookmarks_menu_kb,
                                 delete_bookmark_menu_kb, back_to_bookmarks_kb)


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

    await message.answer(text='Перевести голос в текст?',
                         reply_markup=keyboard)

@router.callback_query(lambda callback: callback.data.startswith('yes:'))
async def voice_transcript(callback: CallbackQuery):
    voice_path = callback.data.split(':')[1]
    transcripted = await voice_to_text(voice_path)
    if os.path.exists(voice_path):
        os.remove(voice_path)
    if transcripted:
        await callback.message.edit_text(text=transcripted)

############################### ПОИСК КВАРТИР ##########################################################
############################### Facebook ###############################################################
@router.message(Text(text=['квартиры', 'Квартиры']))
async def truj_source_choice(message: Message):
    kb = source_choice()
    if message.from_user.id not in user_db:
        print(f'{message.from_user.id} added to DB')
        user_db[message.from_user.id] = deepcopy(user_dict_template)
    user_db[message.from_user.id]['page'] = 1
    await message.answer(text='На каком сайте ищем?',
                         reply_markup=kb)


@router.callback_query(Text(text=['fb', 'adon']))
async def fb_city_choice(callback: CallbackQuery):
    kb = city_choice(callback.data)
    await callback.message.edit_text(text='В каком городе ищем?',
                                     reply_markup=kb)


@router.callback_query(Text(text=['Huanchaco_fb', 'Trujillo_fb', 'Trujillo_adon', 'Huanchaco_adon']))
async def fb_search_result(callback: CallbackQuery):
    city = callback.data.split('_')[0]
    await callback.message.edit_text(text=f'Подождите минутку, ищу квартиры в <b>{LEXICON[city]}</b>',
                                     reply_markup=None)

    pages = main_func(callback.data)
    user_db[callback.from_user.id]['parse_results'] = deepcopy(pages)
    print(user_db[callback.from_user.id]['parse_results'])
    page = user_db[callback.from_user.id]['page']
    text = '\n---\n'.join(user_db[callback.from_user.id]['parse_results'][page])
    await callback.message.edit_text(text = text,
                                  reply_markup=pagination_kb(page, len(user_db[callback.from_user.id]['parse_results'])),
                                  disable_web_page_preview=True)


# "next" handler
@router.callback_query(Text(text='next'))
async def next_page(callback: CallbackQuery):
    if user_db[callback.from_user.id]['page'] < len(user_db[callback.from_user.id]['parse_results']):
        user_db[callback.from_user.id]['page'] += 1
        page = user_db[callback.from_user.id]['page']
        text = '\n---\n'.join(user_db[callback.from_user.id]['parse_results'][page])
        await callback.message.edit_text(text=text,
                                         reply_markup=pagination_kb(page, len(user_db[callback.from_user.id]['parse_results'])),
                                         disable_web_page_preview=True)
    else:
        await callback.message.edit_text(text='Все просмотрено',
                                         reply_markup=begin_or_archive())


# "prev" handler
@router.callback_query(Text(text='prev'))
async def previous_page(callback: CallbackQuery):
    if user_db[callback.from_user.id]['page'] > 1:
        user_db[callback.from_user.id]['page'] -= 1
        page = user_db[callback.from_user.id]['page']
        text = '\n---\n'.join(user_db[callback.from_user.id]['parse_results'][page])
        await callback.message.edit_text(text=text,
                                         reply_markup=pagination_kb(page, len(user_db[callback.from_user.id]['parse_results'])),
                                         disable_web_page_preview=True)
    else:
        pass


# 'bookmarks' handler
@router.callback_query(Text(text='bkmrk'))
async def bookmark_pressed(callback: CallbackQuery):
    page = user_db[callback.from_user.id]['page']
    kb = bookmark_choice(len(user_db[callback.from_user.id]['parse_results'][page]))
    text = '\n---\n'.join(user_db[callback.from_user.id]['parse_results'][page])
    await callback.message.edit_text(text=text + '\n\n<b>Выберите номер объявления для сохранения в архив</b>',
                                     reply_markup=kb,
                                     disable_web_page_preview=True)


# bookmark add
@router.callback_query(lambda x: x.data.startswith('archive'))
async def add_bookmark(callback: CallbackQuery):
    idx = int(callback.data.split(':')[1])
    page = user_db[callback.from_user.id]['page']
    b = user_db[callback.from_user.id]['parse_results'][page][idx]
    user_db[callback.from_user.id]['bookmarks'].add(b)
    print(user_db[callback.from_user.id]['bookmarks'])
    kb = pagination_kb(page, len(user_db[callback.from_user.id]['parse_results']))
    text = '\n---\n'.join(user_db[callback.from_user.id]['parse_results'][page])
    await callback.message.edit_text(text=text + '\n\n<b>Объявление сохранено в архив</b>',
                                     reply_markup=kb,
                                     disable_web_page_preview=True)


#bookmarks menu
@router.callback_query(Text(text='bkmrks'))
async def bookmarks_menu(callback: CallbackQuery):
    data = user_db[callback.from_user.id]['bookmarks']
    kb = bookmarks_menu_kb(*data)
    await callback.message.edit_text(text=f'АРХИВ',
                                     reply_markup=kb,
                                     disable_web_page_preview=True)


# CONTINUE handler
@router.callback_query(Text(text='continue'))
async def continue_read(callback: CallbackQuery):
    page = user_db[callback.from_user.id]['page']
    kb = pagination_kb(page, len(user_db[callback.from_user.id]['parse_results']))
    text = '\n---\n'.join(user_db[callback.from_user.id]['parse_results'][page])
    await callback.message.edit_text(text=text, reply_markup=kb, disable_web_page_preview=True)


# DELETE ALL bookmarks
@router.callback_query(Text(text='delall'))
async def purge_archive(callback: CallbackQuery):
    user_db[callback.from_user.id]['bookmarks'] = set()
    kb = bookmarks_menu_kb()
    await callback.message.edit_text(text='Архив пуст', reply_markup=kb)


# RERUN search handler
@router.callback_query(Text(text='rerun'))
async def rerun_search(callback: CallbackQuery):
    user_db[callback.from_user.id]['page'] = 1
    kb = source_choice()
    await callback.message.edit_text(text='На каком сайте ищем??',
                                     reply_markup=kb)

# FIRST PAGE
@router.callback_query(Text(text='begin'))
async def move_first_page(callback: CallbackQuery):
    user_db[callback.from_user.id]['page'] = 1
    page = user_db[callback.from_user.id]['page']
    text = '\n---\n'.join(user_db[callback.from_user.id]['parse_results'][page])
    await callback.message.edit_text(text=text,
                                     reply_markup=pagination_kb(page, len(user_db[callback.from_user.id]['parse_results'])),
                                     disable_web_page_preview=True)

# LAST PAGE
@router.callback_query(Text(text='to_end'))
async def move_last_page(callback: CallbackQuery):
    user_db[callback.from_user.id]['page'] = len(user_db[callback.from_user.id]['parse_results'])
    page = user_db[callback.from_user.id]['page']
    text = '\n---\n'.join(user_db[callback.from_user.id]['parse_results'][page])
    if text != callback.message.text:
        await callback.message.edit_text(text=text,
                                        reply_markup=pagination_kb(page, len(user_db[callback.from_user.id]['parse_results'])),
                                        disable_web_page_preview=True)
    else:
        await callback.answer()

# DELETE MENU
@router.callback_query(Text(text='del'))
async def delete_bookmark_menu(callback: CallbackQuery):
    archive = user_db[callback.from_user.id]['bookmarks']
    if archive:
        await callback.message.edit_text(text='<b>Выберите закладку для удаления</b>', reply_markup=delete_bookmark_menu_kb(*archive))
    else:
        await callback.message.edit_text(text='Нет закладок для удаления', reply_markup=bookmarks_menu_kb())


# DELETING BOOKMARK
@router.callback_query(Text(startswith='remove:'))
async def delete_bookmark(callback: CallbackQuery):
    idx = int(callback.data.split(':')[1])
    archive = sorted(user_db[callback.from_user.id]['bookmarks'])
    del archive[idx]
    user_db[callback.from_user.id]['bookmarks'] = set(archive)
    await callback.message.edit_text(text='<b>Елемент удален</b>', reply_markup=delete_bookmark_menu_kb(*archive))


# SHOW BOOKMARK
@router.callback_query(Text(startswith='show:'))
async def show_bookmark(callback: CallbackQuery):
    idx = int(callback.data.split(':')[1])
    archive = sorted(user_db[callback.from_user.id]['bookmarks'])
    text = archive[idx]
    kb = back_to_bookmarks_kb()
    await callback.message.edit_text(text=text, reply_markup=kb, disable_web_page_preview=True)


#################################################################################################################
########################### Adondevivir #########################################################################


