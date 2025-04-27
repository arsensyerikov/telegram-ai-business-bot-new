from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("📅 Записатись")],
        [KeyboardButton("💬 Задати питання")],
        [KeyboardButton("📞 Контакти")]
    ],
    resize_keyboard=True
)