import discord
from discord.ext import commands, tasks
import asyncio
import os
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

# Настройка интентов
intents = discord.Intents.default()
intents.members = True
intents.voice_states = True

# Создание бота
bot = commands.Bot(command_prefix="!", intents=intents)

# ID каналов
CHANNEL_ID_1 = 800030268911255553  # Замените на ID первого канала
CHANNEL_ID_2 = 603928470161981442  # Замените на ID второго канала

@bot.event
async def on_ready():
    print(f"Бот запущен как {bot.user}")
    check_ping.start()

@tasks.loop(seconds=10)
async def check_ping():
    for guild in bot.guilds:
        for member in guild.members:
            if member.voice and not member.bot:
                voice_client = member.voice.channel.guild.voice_client
                if voice_client and voice_client.is_connected():
                    ping = voice_client.latency * 1000
                    if ping > 500:
                        try:
                            channel1 = bot.get_channel(CHANNEL_ID_1)
                            channel2 = bot.get_channel(CHANNEL_ID_2)
                            if channel1 and channel2:
                                await member.move_to(channel2)
                                await asyncio.sleep(1)
                                await member.move_to(channel1)
                                print(f"Пользователь {member.name} был перемещён из-за высокого пинга ({ping} мс)")
                        except Exception as e:
                            print(f"Ошибка при перемещении пользователя {member.name}: {e}")

@check_ping.before_loop
async def before_check_ping():
    await bot.wait_until_ready()

# Запуск бота
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    print("Ошибка: Токен не найден. Проверьте переменные окружения.")
else:
    bot.run(TOKEN)
