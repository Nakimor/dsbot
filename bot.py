import os
import discord
from discord.ext import commands, tasks
import asyncio

# Настройка интентов
intents = discord.Intents.default()
intents.message_content = True  # Для работы с содержимым сообщений
intents.members = True          # Для работы с участниками сервера
intents.voice_states = True     # Для работы с голосовыми состояниями

# Создание бота
bot = commands.Bot(command_prefix="!", intents=intents)

# ID каналов
CHANNEL_ID_1 = 800030268911255553  # Первый канал
CHANNEL_ID_2 = 603928470161981442  # Второй канал

# ID пользователя, которого нужно отслеживать
TARGET_USER_ID = 399675455851986974

@bot.event
async def on_ready():
    print(f"Бот запущен как {bot.user}")

@bot.event
async def on_voice_state_update(member, before, after):
    # Проверяем, что это нужный пользователь
    if member.id == TARGET_USER_ID:
        # Проверяем, что пользователь замутил себя (self_mute)
        if after.self_mute and not before.self_mute:
            try:
                # Получаем каналы
                channel1 = bot.get_channel(CHANNEL_ID_1)
                channel2 = bot.get_channel(CHANNEL_ID_2)

                if channel1 and channel2:
                    # Перемещаем пользователя в первый канал
                    await member.move_to(channel1)
                    await asyncio.sleep(0.5)  # Ждём полсекунды

                    # Перемещаем пользователя во второй канал
                    await member.move_to(channel2)
                    await asyncio.sleep(0.5)  # Ждём полсекунды

                    # Перемещаем пользователя обратно во второй канал для надёжности
                    await member.move_to(channel2)
                    print(f"Пользователь {member.name} был перемещён из-за включения self_mute.")
            except Exception as e:
                print(f"Ошибка при перемещении пользователя {member.name}: {e}")

# Запуск бота
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    print("Ошибка: Токен не найден. Проверьте переменные окружения.")
else:
    bot.run(TOKEN)
