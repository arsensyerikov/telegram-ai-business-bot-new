from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN
from handlers import user
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Ініціалізація бота з памʼяттю (для FSM)
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Реєстрація хендлерів
user.register_handlers_user(dp)

# Старт
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)