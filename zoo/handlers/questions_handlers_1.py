import asyncio

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, MessageEntity
from aiogram.fsm.context import FSMContext
from zoo.questions import asks
import zoo.keyboards as kb
from zoo.states import ClientState
from zoo.create_bot import bot
from aiogram.types.input_file import FSInputFile
from zoo.animals import animals

router_quest = Router()

msg_wrong = "Выбран несуществующий вариант,\nвоспользуйтесь кнопками клавиатуры внизу.\n"


def question_handler(i):

    @router_quest.callback_query(F.data.in_(set(list(asks[i].answer_options.values()))), getattr(ClientState, f'l{i}'))
    async def callback_question(callback: CallbackQuery, state: FSMContext):
            user_msg = callback.data
            await state.update_data([(i, user_msg)])
            msg = asks[i+1].question
            await callback.message.answer(msg, reply_markup=kb.in_keyboard(i+1))
            await state.set_state(getattr(ClientState, f'l{i+1}'))

    @router_quest.message(getattr(ClientState, f'l{i}'))
    async def answer_question(message: Message, state: FSMContext) -> None:
        user_msg = message.text
        if user_msg in asks[i].answer_options.values():
            await state.update_data([(i, user_msg)])
            msg = asks[i+1].question
            await message.answer(msg, reply_markup=kb.in_keyboard(i+1))
            await state.set_state(getattr(ClientState, f'l{i+1}'))
        else:
            await message.answer(msg_wrong+asks[i].question, reply_markup=kb.in_keyboard(i))

for i in range(len(asks)-1):
    question_handler(i)

@router_quest.callback_query(F.data.in_(set(list(asks[len(asks)-1].answer_options.values()))), getattr(ClientState, f'l{len(asks)-1}'))
async def callback_end_question(callback: CallbackQuery, state: FSMContext):
    user_msg = callback.data
    await state.update_data([(len(asks)-1, user_msg)])
    await bot.send_photo(chat_id=callback.message.chat.id,
        photo=FSInputFile('zverefic1.png'),
        reply_markup=kb.in_kb_finish,
        caption="Посмотреть результат?")
    await state.set_state(ClientState.WANT_RESULT)

@router_quest.message(getattr(ClientState, f'l{len(asks)-1}'))
async def answer_end_question(message: Message, state: FSMContext):
    user_msg = message.text
    if user_msg in asks[-1].answer_options.values():
        await state.update_data([(len(asks)-1, user_msg)])
        await bot.send_photo(chat_id=message.chat.id,
            photo=FSInputFile('zverefic1.png'),
            reply_markup=kb.in_kb_finish,
            caption="Посмотреть результат?")
        await state.set_state(ClientState.WANT_RESULT)
    else:
        await message.answer(msg_wrong+asks[-1].question, reply_markup=kb.in_keyboard(len(asks)-1))

@router_quest.callback_query(ClientState.WANT_RESULT)
async def callback_get_result(callback: CallbackQuery, state: FSMContext):
    user_msg = callback.data
    if user_msg == "Да":
        data = await state.get_data()
        max = 0
        name = None
        file = None
        result = []
        for i in data:
            if isinstance(i, int):
                result.append(data[i])
        for animal in animals:
            value = animal.compare(result, asks)
            if value > max:
                max = value
                name = animal.name
                file = animal.file

        await state.update_data(file=file, animal_name=name)
        await bot.send_photo(chat_id=callback.message.chat.id, photo=FSInputFile(file),
                             caption=f"Вполне возможно, что Ваше животное - {name}👍")
        await asyncio.sleep(1)
        await bot.send_message(chat_id=callback.message.chat.id, text="Удивлены ?",
                               reply_markup=kb.in_kb_wonder)
        await state.set_state(ClientState.FURTHER_REPEAT)
    else:
        await bot.send_video(
            chat_id=callback.message.chat.id, video=FSInputFile('manu21slow.mp4'), caption="Удачи!")
        await state.clear()

@router_quest.message(ClientState.WANT_RESULT)
async def get_result(message: Message, state: FSMContext):
    user_msg = message.text
    if user_msg in ("Да", "да"):
        data = await state.get_data()
        max = 0
        file = None
        name = None
        result = []
        for i in data:
            if isinstance(i, int):
                result.append(data[i])
        for animal in animals:
            value = animal.compare(result, asks)
            if value > max:
                max = value
                name = animal.name
                file = animal.file
        await state.update_data(file=file, animal_name=name)
        await bot.send_photo(
            chat_id=message.chat.id, photo=FSInputFile(file),
            caption=f"Вполне возможно, что Ваше животное - {name}👍")
        await asyncio.sleep(1)
        await bot.send_message(chat_id=message.chat.id, text="Удивлены ?",
                               reply_markup=kb.in_kb_wonder)
        await state.set_state(ClientState.FURTHER_REPEAT)
    else:
        await message.answer('Вы точно написали не "Да" и не "да", поэтому завершаем сеанс')
        await bot.send_video(
            chat_id=message.chat.id, video=FSInputFile('manu21slow.mp4'),
            caption="Удачи!")
        await state.clear()