import openai
from config import OPENAI_API_KEY
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.main_menu import main_menu
from config import ADMIN_ID
from database.db import add_appointment, get_all_appointments
from config import ADMIN_ID
from database.db import clear_appointments
from aiogram.dispatcher.filters.state import State, StatesGroup
from database.db import update_contacts, get_contacts

# Стан машини (форма)
class Form(StatesGroup):
    name = State()
    service = State()
    datetime = State()
    phone = State()

# Старт
async def start_command(message: types.Message):
    await message.answer("Привіт! Чим я можу допомогти?", reply_markup=main_menu)

# Обробка кнопки "Записатись"
async def start_booking(message: types.Message):
    await Form.name.set()
    await message.answer("Як вас звати?")

async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await Form.next()
    await message.answer("Яку послугу ви бажаєте?", reply_markup=types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton("Масаж спини")],
            [types.KeyboardButton("Релакс масаж")],
            [types.KeyboardButton("Оздоровчий масаж")]
        ], resize_keyboard=True, one_time_keyboard=True
    ))

async def get_service(message: types.Message, state: FSMContext):
    await state.update_data(service=message.text)
    await Form.next()
    await message.answer("На яку дату/час хочете записатись? (наприклад: 25 квітня, 15:00)")

async def get_datetime(message: types.Message, state: FSMContext):
    await state.update_data(datetime=message.text)
    await Form.next()
    await message.answer("Ваш номер телефону?")

async def get_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    data = await state.get_data()
    add_appointment(data['name'], data['service'], data['datetime'], data['phone'])
    await message.answer("Дякуємо! Ми отримали вашу заявку 🙌", reply_markup=main_menu)


    # Надіслати адміну
    text = (
        f"📥 Нова заявка:\n\n"
        f"👤 Імʼя: {data['name']}\n"
        f"🛎 Послуга: {data['service']}\n"
        f"📆 Дата/час: {data['datetime']}\n"
        f"📞 Телефон: {data['phone']}"
    )
    await message.bot.send_message(chat_id=ADMIN_ID, text=text)
    await state.finish()

def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(start_command, commands="start")
    dp.register_message_handler(start_booking, lambda m: m.text == "📅 Записатись")
    dp.register_message_handler(get_name, state=Form.name)
    dp.register_message_handler(get_service, state=Form.service)
    dp.register_message_handler(get_datetime, state=Form.datetime)
    dp.register_message_handler(get_phone, state=Form.phone)
    dp.register_message_handler(send_contacts, lambda m: m.text == "📞 Контакти")
    dp.register_message_handler(start_ai_chat, lambda m: m.text == "💬 Задати питання")
    dp.register_message_handler(handle_ai_question, state="ai_chat")
    dp.register_message_handler(show_appointments, commands="записи")
    dp.register_message_handler(clear_all_appointments, commands="очистити")
    dp.register_message_handler(start_contact_update, commands="налаштування")
    dp.register_message_handler(set_telegram, state=ContactForm.telegram)
    dp.register_message_handler(set_whatsapp, state=ContactForm.whatsapp)
    dp.register_message_handler(set_instagram, state=ContactForm.instagram)



async def send_contacts(message: types.Message):
    contacts = get_contacts()
    if not contacts:
        await message.answer("Контакти ще не налаштовані.")
        return
    text = (
        "📲 Контакти:\n\n"
        f"💬 Telegram: {contacts[0]}\n"
        f"📞 WhatsApp: {contacts[1]}\n"
        f"📸 Instagram: {contacts[2]}"
    )
    await message.answer(text)


# Словник псевдо-AI
faq_responses = {
    "ціна": "💸 Наші послуги від 500 грн. Уточніть конкретну послугу 🙌",
    "адреса": "📍 Ми знаходимось на вул. Шевченка 25, офіс 3.",
    "графік": "🕒 Працюємо з 10:00 до 20:00 щодня, окрім неділі.",
    "привіт": "Вітаю! Я ваш AI-помічник. Як можу допомогти?"
}

# Почати AI-чат
async def start_ai_chat(message: types.Message, state: FSMContext):
    await state.set_state("ai_chat")
    await message.answer("💬 Напишіть своє питання:")

# Відповідь AI
# Псевдо-AI відповіді
faq_responses = {
    "ціна": "💸 Наші послуги від 500 грн. Уточніть конкретну послугу 🙌",
    "вартість": "💸 Залежить від послуги. Напишіть, що вас цікавить!",
    "адреса": "📍 Ми знаходимось на вул. Шевченка 25, офіс 3.",
    "графік": "🕒 Працюємо з 10:00 до 20:00 щодня, окрім неділі.",
    "привіт": "Привіт! Я ваш бот-помічник. Як можу допомогти?"
}

async def handle_ai_question(message: types.Message, state: FSMContext):
    await state.finish()
    text = message.text.lower()
    reply = None
    for keyword, answer in faq_responses.items():
        if keyword in text:
            reply = answer
            break
    if reply:
        await message.answer(reply)
    else:
        await message.answer("🤖 Вибач, я ще вчуся. Спробуй інакше сформулювати питання.")


async def show_appointments(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    appointments = get_all_appointments()
    if not appointments:
        await message.answer("Записів поки немає.")
        return
    text = "📋 Усі записи:\n\n"
    for app in appointments:
        text += (
            f"👤 {app[1]}\n🛎 {app[2]}\n📅 {app[3]}\n📞 {app[4]}\n\n"
        )
    await message.answer(text)


async def clear_all_appointments(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    clear_appointments()
    await message.answer("✅ Усі записи очищено.")

class ContactForm(StatesGroup):
    telegram = State()
    whatsapp = State()
    instagram = State()


async def start_contact_update(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return
    await state.set_state(ContactForm.telegram)
    await message.answer("Введи новий Telegram (наприклад: @yourname)")

async def set_telegram(message: types.Message, state: FSMContext):
    await state.update_data(telegram=message.text)
    await state.set_state(ContactForm.whatsapp)
    await message.answer("Введи WhatsApp (наприклад: +380501234567)")

async def set_whatsapp(message: types.Message, state: FSMContext):
    await state.update_data(whatsapp=message.text)
    await state.set_state(ContactForm.instagram)
    await message.answer("Введи Instagram (наприклад: @yourbusiness)")

async def set_instagram(message: types.Message, state: FSMContext):
    data = await state.update_data(instagram=message.text)
    d = await state.get_data()
    update_contacts(d['telegram'], d['whatsapp'], d['instagram'])
    await message.answer("✅ Контакти оновлено!")
    await state.finish()