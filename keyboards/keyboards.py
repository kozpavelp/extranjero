from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON
from datetime import datetime

def city_choice(source) -> InlineKeyboardMarkup:
    if source == 'fb':
        url = ['Trujillo_fb', 'Huanchaco_fb']
    elif source == 'adon':
        url = ['Trujillo_adon', 'Huanchaco_adon']
    btn_truj: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON['Trujillo'], callback_data=url[0])
    btn_huan: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON['Huanchaco'], callback_data=url[1])
    kb: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[btn_huan], [btn_truj]])
    return kb


def source_choice() -> InlineKeyboardMarkup:
    btn_fb: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON['fb'], callback_data='fb')
    btn_adon: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON['adon'], callback_data='adon')
    kb: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[btn_adon, btn_fb]])
    return kb


def pagination_kb(current, n) -> InlineKeyboardMarkup:
    # upper
    btn_next: InlineKeyboardButton = InlineKeyboardButton(text='>>>',
                                                          callback_data='next')
    btn_mid: InlineKeyboardButton = InlineKeyboardButton(text=f'{current}/{n}',
                                                         callback_data='bkmrk')
    btn_prev: InlineKeyboardButton = InlineKeyboardButton(text='<<<',
                                                          callback_data = 'prev')
    # lower
    btn_bkmrks: InlineKeyboardButton = InlineKeyboardButton(text='Архив',
                                                            callback_data='bkmrks')
    btn_begin: InlineKeyboardButton = InlineKeyboardButton(text='Начало',
                                                           callback_data='begin')
    btn_end: InlineKeyboardButton = InlineKeyboardButton(text='Конец',
                                                         callback_data='to_end')
    btn_rerun: InlineKeyboardButton = InlineKeyboardButton(text='Начать поиск заново',
                                                           callback_data='rerun')

    kb: InlineKeyboardMarkup = InlineKeyboardMarkup(width=3, inline_keyboard=[[btn_prev, btn_mid, btn_next],[btn_begin, btn_bkmrks,btn_end], [btn_rerun]])
    return kb


def begin_or_archive() -> InlineKeyboardMarkup:
    btn_zero: InlineKeyboardButton = InlineKeyboardButton(text='В начало',
                                                          callback_data='begin')
    btn_bkmrks: InlineKeyboardButton = InlineKeyboardButton(text='Закладки',
                                                            callback_data='bkmrks')
    btn_rerun: InlineKeyboardButton = InlineKeyboardButton(text='Начать поиск заново',
                                                           callback_data='rerun')
    kb: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[btn_bkmrks, btn_zero], [btn_rerun]])
    return kb


def bookmark_choice(num: int) -> InlineKeyboardMarkup:
    kbb: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for btn in range(num):
        kbb.row(InlineKeyboardButton(text=str(btn + 1),
                                     callback_data=f'archive:{btn}'
                                     ))
    kbb.adjust(num, 1)
    return kbb.as_markup()


def bookmarks_menu_kb(*args) -> InlineKeyboardMarkup:
    kbb: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Кнопки закладок
    if args:
        sorted_archive = sorted(args)
        for num, bkmrk in enumerate(sorted_archive):
            kbb.row(InlineKeyboardButton(text=f'{num+1}:{bkmrk}',
                                        callback_data=f'show:{num}'
                                        ))
    else:
        btn_rerun: InlineKeyboardButton = InlineKeyboardButton(text='Начать поиск заново',
                                                               callback_data='rerun')
        kbb.row(btn_rerun)
    # навигация
    btn_cont: InlineKeyboardButton = InlineKeyboardButton(text='Продолжить', callback_data='continue')
    btn_del: InlineKeyboardButton = InlineKeyboardButton(text='Редактировать', callback_data='del')
    btn_delall: InlineKeyboardButton = InlineKeyboardButton(text='Очистить архив', callback_data='delall')
    kbb.row(btn_del, btn_cont, btn_delall)

    return kbb.as_markup()


def delete_bookmark_menu_kb(*args):
    kbb: InlineKeyboardBuilder = InlineKeyboardBuilder()
    sorted_archive = sorted(args)
    for num, bkmrk in enumerate(sorted_archive):
        kbb.row(InlineKeyboardButton(text=f"{LEXICON['del']} - {bkmrk}",
                                     callback_data=f'remove:{num}'
                                     ))
    btn_back: InlineKeyboardButton = InlineKeyboardButton(text="Назад", callback_data='bkmrks')
    kbb.row(btn_back)
    return kbb.as_markup()

def back_to_bookmarks_kb():
    btn_back: InlineKeyboardButton = InlineKeyboardButton(text='Назад к архиву', callback_data='bkmrks')
    btn_cont: InlineKeyboardButton = InlineKeyboardButton(text='Продолжить просмотр', callback_data='continue')
    kb: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[btn_back, btn_cont]])
    return kb



