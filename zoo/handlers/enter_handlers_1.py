from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from zoo.questions import asks
import zoo.keyboards as kb
from zoo.states import ClientState
from aiogram.filters import CommandStart
from aiogram.types.input_file import FSInputFile
from zoo.create_bot import bot
import aiosqlite as sq

router_enter = Router()


@router_enter.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    name = message.from_user.full_name
    date = message.date
    db = await sq.connect('my_base.sqlite3')
    cur = await db.cursor()
    await cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, "
                      "user_id INTEGER, "
                      "name VARCHAR(20), "
                      "date BIGINT, "
                      "feedback TEXT)")


    await db.commit()

    await cur.execute(f"INSERT INTO users (user_id, name, date) VALUES ('{user_id}', '{name}', '{date}')")
    await db.commit()
    await cur.close()
    await db.close()


    await state.update_data(user_id=user_id, name=name, date=date)
    await state.set_state(ClientState.PRESSED_START)
    await bot.send_photo(chat_id=message.chat.id,
        photo=FSInputFile('MZoo-logo since 1864-vert-eng_preview-01.jpg'),
        reply_markup=kb.in_kb_go,
        caption='Примите участие в викторине Московского зоопарка!\n\
Ответьте на несколько вопросов и узнайте,\nкакое животное "живет" внутри Вас.\n\
Начнем:')
    await message.delete()


@router_enter.callback_query(F.data.in_({'Go', 'Repeat'}))
async def callback_go_cmd(callback: CallbackQuery, state: FSMContext):
    msg = asks[0].question
    await callback.message.answer(msg, reply_markup=kb.in_keyboard(0))
    await state.set_state(getattr(ClientState, 'l0'))


@router_enter.message(ClientState.PRESSED_START)
async def answer_go_cmd(message: Message, state: FSMContext):
    if message.text in ('/Go', '/go', '/GO', 'Go', 'go', 'GO'):
            msg = asks[0].question
            await message.answer(msg, reply_markup=kb.in_keyboard(0))
            await state.set_state(getattr(ClientState, 'l0'))
    else:
            await message.answer('Команда неверная. Нажмите на кнопку "Поехали!".', reply_markup=kb.in_kb_go)