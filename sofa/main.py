from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database.database import User
from markups import start_markup, registation_markup, again_registration
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State


bot = Bot(token="7132803658:AAF-e7djEMkUQyrtvUNMQk6zdkFArUxbWes")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=MemoryStorage())


class AwaitMessages(StatesGroup):
    name = State()
    lastname = State()
    age = State()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    if not User().check_user_exists(message.chat.id):
        User().add_user(message.chat.id)
    await message.answer(f"Здравствуйте, {message.chat.first_name}! Для регистрации на мероприятие нажмите кнопку регистрация", reply_markup=start_markup)


@dp.callback_query_handler(text_startswith="cancel") 
async def registration(call:types.CallbackQuery):
    if not User().is_user_registered(call.message.chat.id):
        await call.message.edit_text("Введите ваше имя")
        await AwaitMessages.name.set()
    else:
        await call.message.edit_text(f"Вы уже зарегистрированы.")

@dp.callback_query_handler(text_startswith="again") 
async def registration(call:types.CallbackQuery):
    await call.message.edit_text("Введите ваше имя")
    await AwaitMessages.name.set()

@dp.callback_query_handler(text_startswith="accept") 
async def registration(call:types.CallbackQuery):
    await call.message.edit_text("Вы успешно зарегистрировались")
    User().register_user(call.message.chat.id)

@dp.message_handler(state=AwaitMessages.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await message.answer('Введите вашу фамилию.')
    await AwaitMessages.lastname.set()

@dp.message_handler(state=AwaitMessages.lastname)
async def process_lastname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['lastname'] = message.text

    await message.answer('Введите ваш возраст.')
    await AwaitMessages.age.set()

@dp.message_handler(state=AwaitMessages.age)
async def process_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text
        await message.answer(f'Ваша заявка на регистрацию:\nВозраст - {data["age"]}\nИмя,Фамилия - {data["name"]} {data["lastname"]}', reply_markup=registation_markup)
        await state.finish()



@dp.message_handler()
async def idk(message: types.Message):
    await message.answer("Я не понимаю эту команду, для регистрации используйте /start")



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)