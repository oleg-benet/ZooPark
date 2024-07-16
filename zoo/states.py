from aiogram.fsm.state import StatesGroup, State
from questions import asks

l = []


class ClientState(StatesGroup):
    for i in range(len(asks)+5):
        l.append(f'l{i}=State()')
    for i in l:
        exec(i)
    PRESSED_START = State()
    WANT_RESULT = State()
    FURTHER_REPEAT = State()
    PROGRAM = State()
    CLOSE = State()
    CHOOSE_NETWORK = State()
    OPTIONS = State()
    WRITTEN = State()
    SENDING = State()
    FEED = State()
