import discord
from discord.ext import commands
import yt_dlp
import os

# Konfiguracja
TOKEN = os.environ.get('DISCORD_TOKEN') # Ustaw to w zmiennych środowiskowych serwera
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Ustawienia yt_dlp (Silnik wyszukiwania)
YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'noplaylist': True,
    'quiet': True,
    'default_search': 'auto', # Automatycznie szuka na YT, nawet jeśli dasz link Spotify
}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

@bot.event
async def on_ready():
    print(f"🐾 Nadzieja (Python) gotowa! Wersja: 4.0")

@bot.command(name="play")
async def play(ctx, *, search: str):
    if not ctx.author.voice:
        return await ctx.send("❌ Musisz być na kanale głosowym!")
    
    channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await channel.connect()
    
    async with ctx.typing():
        with yt_dlp.YoutubeDL(YTDL_OPTIONS) as ydl:
            # Wyszukiwanie muzyki
            info = ydl.extract_info(f"ytsearch:{search}", download=False)['entries'][0]
            url = info['url']
            title = info['title']
            duration = info.get('duration', 0)

        # Odtwarzanie
        source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
        ctx.voice_client.stop()
        ctx.voice_client.play(source)

    # Śliczny Embed z Twoim zdjęciem
    embed = discord.Embed(
        title="🎵 Teraz gram (Python Edition)",
        description=f"**{title}**\n`Długość: {duration // 60}:{duration % 60:02d}`",
        color=0x2b7fff
    )
    embed.set_image(url="https://i.imgur.com/K3Z9X5u.jpeg")
    embed.set_footer(text="Nadzieja • Python 🐾")
    
    await ctx.send(embed=embed)

@bot.command(name="stop")
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("🛑 Nadzieja kończy granie. *Nya~!*")

bot.run(TOKEN)
