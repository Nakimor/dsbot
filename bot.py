import os
import discord
from discord.ext import commands, tasks
import asyncio

# Настройка интентов
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

# Создание бота
bot = commands.Bot(command_prefix="!", intents=intents)

# ID канала для периодических сообщений
CHANNEL_ID_FOR_MESSAGES = 1104013436536492060

# ID каналов для перемещения
CHANNEL_ID_1 = 800030268911255553  # Первый канал
CHANNEL_ID_2 = 603928470161981442  # Второй канал

# ID пользователя, которого нужно отслеживать
TARGET_USER_ID = 399675455851986974

@bot.event
async def on_ready():
    print(f"Бот запущен как {bot.user}")
    
    # Установка статуса и активности
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="за мутами участников"
        ),
        status=discord.Status.online
    )
    
    # Запуск задачи для отправки периодических сообщений
    send_periodic_message.start()

@bot.event
async def on_voice_state_update(member, before, after):
    if member.id == TARGET_USER_ID:
        if after.self_mute and not before.self_mute:
            try:
                channel1 = bot.get_channel(CHANNEL_ID_1)
                channel2 = bot.get_channel(CHANNEL_ID_2)

                if channel1 and channel2:
                    await member.move_to(channel1)
                    await asyncio.sleep(0.5)
                    await member.move_to(channel2)
                    await asyncio.sleep(0.5)
                    await member.move_to(channel2)
                    print(f"Пользователь {member.name} был перемещён из-за включения self_mute.")
            except Exception as e:
                print(f"Ошибка при перемещении пользователя {member.name}: {e}")

@tasks.loop(seconds=25)
async def send_periodic_message():
    try:
        channel = bot.get_channel(CHANNEL_ID_FOR_MESSAGES)
        if channel:
            await channel.send("Привет! Я всё ещё здесь и слежу за мутами участников. 😊")
        else:
            print("Канал для сообщений не найден.")
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")

@send_periodic_message.before_loop
async def before_send_periodic_message():
    await bot.wait_until_ready()

# Запуск бота
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    print("Ошибка: Токен не найден. Проверьте переменные окружения.")
else:
    bot.run(TOKEN)
