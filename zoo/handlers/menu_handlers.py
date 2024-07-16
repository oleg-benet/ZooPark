from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import zoo.keyboards as kb
from zoo.states import ClientState
from zoo.create_bot import bot
from aiogram.types.input_file import FSInputFile
from zoo.smtp import send_mail
import asyncio
import aiosqlite as sq

router_options = Router()

text_options = "Если у Вас возникли вопросы относительно программы опеки или есть желание оставить\
 свой отзыв о работе нашего бота, воспользуйтесь меню"

@router_options.callback_query(F.data == 'Finish',ClientState.CLOSE)
async def callback_end(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text_options, reply_markup=kb.in_menu)
    await state.set_state(ClientState.OPTIONS)

@router_options.message(ClientState.CLOSE)
async def message_end_all(message: Message, state: FSMContext):
    await message.answer("Похоже, Вы хотели завершить сеанс. Это меню для обратной связи", reply_markup=kb.in_menu)
    await state.set_state(ClientState.OPTIONS)


@router_options.callback_query(F.data == 'feedback', ClientState.OPTIONS)
async def callback_feedback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Напишите и отправьте отзыв")
    await state.set_state(ClientState.FEED)


@router_options.message(ClientState.FEED)
async def message_feedback(message: Message, state: FSMContext):
    feedback = message.text
    await state.update_data(feedback=feedback)
    data = await state.get_data()
    db = await sq.connect('my_base.sqlite3')
    cur = await db.cursor()
    await cur.execute(f"UPDATE users SET feedback = '{feedback}' "
                      f"WHERE user_id = '{message.from_user.id}' AND date = '{data['date']}'")
    await db.commit()
    await cur.close()
    await db.close()
    await message.answer("Отзыв отправлен", reply_markup=kb.in_menu)
    await state.set_state(ClientState.OPTIONS)


@router_options.callback_query(F.data == 'email', ClientState.OPTIONS)
async def callback_email(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Наберите текст письма, после ввода которого, Вам будет предложено подтвердить "
"отправку или отказаться от нее:")
    await state.set_state(ClientState.WRITTEN)


@router_options.callback_query(F.data == 'phone', ClientState.OPTIONS)
async def callback_email(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(f'Дежурный по зоопарку\n +79039480597')


@router_options.message(ClientState.WRITTEN)
async def message_end_all(message: Message, state: FSMContext):
    letter = message.text
    await state.update_data(letter=letter)
    await message.answer("Отправить?", reply_markup=kb.in_kb_sending)
    await state.set_state(ClientState.SENDING)


@router_options.callback_query(F.data == 'send', ClientState.SENDING)
async def callback_feedback(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data['user_id']
    name = data['name']
    letter = data['letter']
    await callback.message.answer("Письмо отправлено", reply_markup=kb.in_menu)
    await send_mail(f'Сообщение от пользователя {name} с ID = {user_id}', 'benetal@yandex.ru',
                          f'<h3>{letter}</h3>\n {data} ')
    await state.set_state(ClientState.OPTIONS)

@router_options.callback_query(F.data == 'cancel', ClientState.SENDING)
async def callback_feedback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Новая попытка выбора", reply_markup=kb.in_menu)
    await state.set_state(ClientState.OPTIONS)


@router_options.callback_query(F.data == 'Exit')
async def callback_exit(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await bot.send_video(
        chat_id=callback.message.chat.id, video=FSInputFile('manu21slow.mp4'),
        caption="Удачи!")

@router_options.message(ClientState.OPTIONS)
async def message_err(message: Message, state: FSMContext):
    await message.answer("Ошибочное действие", reply_markup=kb.in_menu)
