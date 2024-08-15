from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import zoo.keyboards as kb
from zoo.states import ClientState
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()
access_token = os.getenv('access_token')

router_cust = Router()

text_dis = ("Может быть, Вы не разделяете наш вывод и Ваши ощущения склоняются к другому животному – это объясняется тем,\
что мы используем «средневзвешенный»  подход к оценке ответов. А взвешиваем мы на их на ста-а-ареньких \
«айболитовских» весах. Для исправления ситуации и достижения внутренней  гармонии Вы можете лично взглянуть\
 на обитателей нашего зоопарка и присмотреть более подходящего для себя животного. Возможно, оно произведет на Вас\
 глубокое впечатление и Вы захотите поучаствовать в нашей программе опеки. Это достойное дело для добрых людей.\
 Давайте ознакомимся с программой?")

text_custody = ("Опекунство в Московском зоопарке\n\
Возьмите животное под опеку!\n\
Участие в программе «Клуб друзей зоопарка» — это помощь в содержании наших\n\
обитателей, а также ваш личный вклад в дело сохранения биоразнообразия Земли и\n\
развитие нашего зоопарка.\n\
Основная задача Московского зоопарка с самого начала его существования это —\n\
сохранение биоразнообразия планеты. Когда вы берете под опеку животное, вы помогаете\n\
нам в этом благородном деле. При нынешних темпах развития цивилизации к 2050 году с\n\
лица Земли могут исчезнуть около 10 000 биологических видов. Московский зоопарк\n\
вместе с другими зоопарками мира делает все возможное, чтобы сохранить их.\
Традиция опекать животных в Московском зоопарке возникло с момента его создания в\n\
1864г. Такая практика есть и в других зоопарках по всему миру.\n\
В настоящее время опекуны объединились в неформальное сообщество — Клуб друзей\n\
Московского зоопарка. Программа «Клуб друзей» дает возможность опекунам ощутить\n\
свою причастность к делу сохранения природы, участвовать в жизни Московского\n\
зоопарка и его обитателей, видеть конкретные результаты своей деятельности.\n\
Опекать – значит помогать любимым животным. Можно взять под крыло любого\n\
обитателя Московского зоопарка, в том числе и того, кто живет за городом – в\n\
Центре воспроизводства редких видов животных под Волоколамском. Там живут и\n\
размножаются виды, которых нет в городской части зоопарка: величественные журавли\n\
стерхи, забавные дрофы, исчезнувшая в природе лошадь Пржевальского, изящные\n\
антилопы бонго и многие другие. Можете съездить на экскурсию в Центр и познакомиться\n\
с обитателями.")

text_share = "Выберите из списка социальную сеть"


@router_cust.callback_query(F.data == 'Continue', ClientState.FURTHER_REPEAT)
async def callback_continue(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text_dis, reply_markup=kb.in_kb_custody)
    await state.set_state(ClientState.PROGRAM)


@router_cust.message(ClientState.FURTHER_REPEAT)
async def lets_continue(message: Message, state: FSMContext):
    if message.text == 'Следуем дальше':
        await message.answer(text_dis, reply_markup=kb.in_kb_custody)
        await state.set_state(ClientState.PROGRAM)
    else:
        await message.answer(text='Неверная команда. Воспользуйтесь клавиатурой.', reply_markup=kb.in_kb_wonder)


@router_cust.callback_query(F.data == 'Share', ClientState.FURTHER_REPEAT)
async def callback_share(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text_share, reply_markup=kb.in_soc_network)
    await state.set_state(ClientState.CHOOSE_NETWORK)


@router_cust.callback_query(F.data == 'Empty', ClientState.CHOOSE_NETWORK)
async def callback_share(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Это резервная кнопка")
    #time.sleep(2)
    await callback.message.answer("Продолжаем тур", reply_markup=kb.in_kb_custody)
    await state.set_state(ClientState.PROGRAM)


@router_cust.callback_query(F.data == 'VK', ClientState.CHOOSE_NETWORK)
async def callback_share(callback: CallbackQuery, state: FSMContext):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                url='https://api.vk.com/method/photos.getWallUploadServer',
                headers=[('Connection', 'close')],
                params={
                    'access_token': access_token,
                    'v': '11.9.9'
                }
        ) as address_query:
            address_query_json = await address_query.json()
            upload_url = address_query_json['response']['upload_url']

        # async with aiofiles.open("dolphin.jpg", mode='rb') as file:
        #     data = {'file': file}
        data = await state.get_data()
        img = data['file']

        with open(img, mode='rb') as file:
            data = {'file': file}

            async with session.post(url=upload_url, headers=[('Connection', 'close')], data=data) as response:
                response_json = await response.json()
                print(response_json)

        async with session.post(url='https://api.vk.com/method/photos.saveWallPhoto',
                                headers=[('Connection', 'close')],
                                params={
                                    'photo': response_json['photo'],
                                    'server': response_json['server'],
                                    'access_token': access_token,
                                    'hash': response_json['hash'],
                                    'v': '11.9.9'
                                }
                                ) as response:
            response_json = await response.json()
            print(response_json)
            saved_photo = "photo" + str(response_json['response'][0]['owner_id']) + "_" + str(
                response_json['response'][0]['id'])
            print(saved_photo)

        await session.post(url='https://api.vk.com/method/wall.post',
                           headers=[('Connection', 'close')],
                           params={
                               'access_token': access_token,
                               'attachments': 'https://t.me/AnyAnimalsBot',
                               'v': '11.9.9'
                           }
                           )

        await session.post(url='https://api.vk.com/method/wall.post',
                           headers=[('Connection', 'close')],
                           params={
                               'access_token': access_token,
                               'message': 'Вот такой получился зверь. Узнайте своего по ссылке "Зоовикторина"',
                               'attachments': saved_photo,
                               'v': '11.9.9'
                           }
                           )

    await callback.message.answer("Продолжаем тур", reply_markup=kb.in_kb_custody)
    await state.set_state(ClientState.PROGRAM)

@router_cust.message(ClientState.CHOOSE_NETWORK)
async def message_program(message: Message, state: FSMContext):
    await message.answer("Выберите еще раз",reply_markup=kb.in_kb_wonder)
    await state.set_state(ClientState.FURTHER_REPEAT)


@router_cust.callback_query(F.data == 'Program', ClientState.PROGRAM)
async def callback_program(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text_custody, reply_markup=kb.in_kb_site)
    await state.set_state(ClientState.CLOSE)


@router_cust.message(ClientState.PROGRAM)
async def message_program(message: Message, state: FSMContext):
    if message.text == 'Наша программа опеки':
        await message.answer(text_dis, reply_markup=kb.in_kb_site)
        await state.set_state(ClientState.CLOSE)
    else:
        await message.answer(text='Неверная команда', reply_markup=kb.in_kb_custody_rep)


