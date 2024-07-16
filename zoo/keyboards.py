from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton )
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from questions import asks

in_kb_go = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Поехали', callback_data='Go')]])


def in_keyboard(ask):
    keyboard = InlineKeyboardBuilder()
    dict = asks[ask].answer_options
    for variant in dict.keys():
        keyboard.add(InlineKeyboardButton(text=variant, callback_data=dict[variant]))
    return keyboard.adjust(2).as_markup()

in_kb_finish = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да', callback_data='Да'), InlineKeyboardButton(text='Нет', callback_data='Нет')]
])

in_kb_wonder = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton (text='Следуем дальше', callback_data='Continue'),
     InlineKeyboardButton(text='Попробовать еще раз', callback_data='Repeat')],
    [InlineKeyboardButton (text='Поделиться результатом в соцсети', callback_data='Share')]
])

in_kb_custody = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Наша программа опеки', callback_data='Program')]
])

in_kb_custody_rep = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Обзор программы?', callback_data='Program'),
    InlineKeyboardButton (text='Или выйти?', callback_data='Exit')]
])

in_kb_site = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Перейти на сайт', url="https://new.moscowzoo.ru/about/guardianship"),
    InlineKeyboardButton(text='Перейти на тг-канал', url="https://t.me/s/Moscowzoo_official")],

    [InlineKeyboardButton(text='Завершить сеанс', callback_data='Finish')]
])

in_soc_network = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Резерв', callback_data='Empty'),
     InlineKeyboardButton(text='VK', callback_data='VK')],
    [InlineKeyboardButton(text='Резерв', callback_data='Empty'),
     InlineKeyboardButton(text='Резерв', callback_data='Empty')],
])

in_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Оставить отзыв', callback_data='feedback')],
    [InlineKeyboardButton(text='Отправить письмо сотруднику', callback_data='email')],
    [InlineKeyboardButton(text='Позвонить сотруднику', callback_data='phone')],
    [InlineKeyboardButton(text='Собственно выход', callback_data='Exit')],
])

in_kb_sending = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да', callback_data='send')],
    [InlineKeyboardButton (text='Нет', callback_data='cancel')]
])