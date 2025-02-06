import os.path
import sys
import logging
import asyncio
import json
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ContentType, Update
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# Токен для бота
TOKEN = ""

# Инициализация бота с передачей default настроек
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()

#def load_last_messages_update_id():
#    if not os.path.exists("Last_Messages_update_id.json"):
#        save_last_messages_update_id(0)
#        return 0

#    try:
#        with open("Last_Messages_update_id.json", encoding="UTF-8") as files_in:
#            data = json.load(files_in)
#            return data.get("Last_message_update_id", 0)
#    except (FileNotFoundError, json.JSONDecodeError):
#        return 0


#def save_last_messages_update_id(update_id):
#    with open("Last_Messages_update_id.json", "w", encoding="UTF-8") as files_in:
#        return json.dump({"Last_message_update_id": update_id}, files_in, ensure_ascii=False, indent=4)

def load_stats():
    try:
        with open("Database.json", encoding="UTF-8") as file_in:
            return json.load(file_in)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_stats():
    with open("Database.json", "w", encoding="UTF-8") as file_in:
        return json.dump(user_statistics, file_in, ensure_ascii=False, indent=4)


user_statistics = load_stats()

#last_update_id = load_last_messages_update_id()

# Хэндлер для команды /stat
@dp.message(Command("stat", ignore_case=True, prefix="/"))
async def stats(message: Message):
    user_id = str(message.from_user.id)
    stats = user_statistics.get(user_id, {"messages": 0, "stickers": 0, "voice": 0, "photo": 0, "video": 0})

    await message.answer(f"Статистика юзверя {message.from_user.username}\n"
                         f"Отправлено сообщений: {stats['messages']}\n"
                         f"Отправлено стикеров: {stats['stickers']}\n"
                         f"Отправлено ГС: {stats['voice']}\n"
                         f"Отправлено фото: {stats['photo']}\n"
                         f"Отправлено видео: {stats['video']}\n")



#@dp.update()
#async def handle_update(update: Update):
#    print(f"Update ID: {Update.update_id}")
#    global last_update_id
#    if update.update_id <= last_update_id:
#        return  # пропуск старых сообщений
#
#    last_update_id = Update.update_id
#    save_last_messages_update_id(update.update_id)


# Хэндлер для всех сообщений
@dp.message()
async def count_messages(message: Message):
    user_id = str(message.from_user.id)  # Получение user_id
    if user_id not in user_statistics:
        user_statistics[user_id] = {"messages": 0, "stickers": 0, "voice": 0, "photo": 0, "video": 0}
    if message.content_type == ContentType.TEXT:
        user_statistics[user_id]["messages"] += 1
    elif message.content_type == ContentType.STICKER:
        user_statistics[user_id]["stickers"] += 1
    elif message.content_type == ContentType.VOICE:
        user_statistics[user_id]["voice"] += 1
    elif message.content_type == ContentType.PHOTO:
        user_statistics[user_id]["photo"] += 1
    elif message.content_type == ContentType.VIDEO:
        user_statistics[user_id]["video"] += 1
    save_stats()
# Запуск бота
async def main() -> None:

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)#логирование только для деббага,иначе большая нагрузка выходит
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')


