from aiogram import types



registation_markup = types.InlineKeyboardMarkup(row_width=1)

registation_markup.add(types.InlineKeyboardButton("Зарегистрироваться✅", callback_data="accept"))
registation_markup.add(types.InlineKeyboardButton("Отменить❌", callback_data="again"))

start_markup = types.InlineKeyboardMarkup(row_width=1)
start_markup.add(types.InlineKeyboardButton("Пройти регистрацию", callback_data="cancel"))

again_registration = types.InlineKeyboardMarkup(row_width=1)
again_registration.add(types.InlineKeyboardButton("Пройти заного", callback_data="again"))