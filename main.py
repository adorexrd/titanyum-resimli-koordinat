import discord
from discord.ext import commands
from discord import app_commands
from pymongo import MongoClient
import math
import re
import asyncio
from io import BytesIO
from datetime import datetime
import easyocr
import numpy as np
from PIL import Image

# CONFIG
TOKEN = "TOKEN"
MONGO_URI = "MONGO_URI"
KODUN_CALISACAGI_KANAL_ID = 1411309635612184697 # Buraya kanal ID'sini girin

# EasyOCR okuyucusunu başlat (Türkçe ve İngilizce dillerini tanır)
reader = easyocr.Reader(['tr', 'en'])

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
client = MongoClient(MONGO_URI)
db = client["titanyum"]
hesaplar = db["hesaplar"]

@bot.event
async def on_ready():
    await bot.tree.sync()
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name="Adorexrd ❤"))
    print(f"Bot giriş yaptı: {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user or not message.attachments:
        return
    
    if message.channel.id != KODUN_CALISACAGI_KANAL_ID:
        return

    for attachment in message.attachments:
        if attachment.content_type.startswith("image/"):
            await message.channel.send("Ekran görüntüsü inceleniyor... Lütfen bekleyin.")

            try:
                image_bytes = await attachment.read()
                image = Image.open(BytesIO(image_bytes)).convert("RGB")
                image_np = np.array(image)

                result = reader.readtext(image_np)
                
                full_text = " ".join([item[1] for item in result])
                print(f"EasyOCR Tarafından Okunan Metin:\n{full_text}\n---")
                
                await process_image_text(message, full_text, attachment.url)
            except Exception as e:
                print(f"Hata oluştu: {e}")
                await message.channel.send("❌ Resim işlenirken bir hata oluştu.")
                
    await bot.process_commands(message)

async def process_image_text(message, text, image_url):
    # Koordinatları bulma
    coord_match = re.search(r"X:\s*(-?\d+)\s+Y:\s*(-?\d+)\s+Z:\s*(-?\d+)", text, re.IGNORECASE)
    if not coord_match:
        await message.channel.send("❌ Koordinatlar ekran görüntüsünde bulunamadı.")
        return
    
    x, z = int(coord_match.group(1)), int(coord_match.group(3))

    # Dünya adını bulma
    dunya_adi_match = re.search(r"D[u|ü|i]nya:\s*([a-zA-Z]+)", text, re.IGNORECASE)
    dunya_adi = None
    if dunya_adi_match:
        dunya_adi = dunya_adi_match.group(1).lower()
        valid_dunyalar = ["sancak", "yakamoz", "avrasya", "pruva", "velena", "flador", "astra"]
        if dunya_adi not in valid_dunyalar:
            dunya_adi = None

    # Kalan zamanı bulma
    kalan_zaman = "Bilgi yok"
    kalan_zaman_match = re.search(r"Kalan Z[a|e|ı]man:\s*(\S+)", text, re.IGNORECASE)
    if kalan_zaman_match:
        kalan_zaman = kalan_zaman_match.group(1)

    # Claim sayısını bulma
    claim_sayisi = "Bilgi yok"
    claim_match = re.search(r"B[o|ö]lge S[a|ay][y|ı]s[ı|i]:\s*(\S+)", text, re.IGNORECASE)
    if claim_match:
        claim_sayisi = claim_match.group(1)
        
    if dunya_adi:
        await find_and_send_results(message, dunya_adi, x, z, kalan_zaman, claim_sayisi, image_url)
    else:
        await ask_for_world(message, x, z, kalan_zaman, claim_sayisi, image_url)

async def ask_for_world(message, x, z, kalan_zaman, claim_sayisi, image_url):
    soru_mesaj = await message.channel.send("🤔 **Dünya adı bulunamadı.** Lütfen hangi dünyadan olduğunu yaz.")

    def check(m):
        return m.author == message.author and m.channel == message.channel

    try:
        cevap = await bot.wait_for('message', check=check, timeout=60.0)
        dunya_adi = cevap.content.strip().lower()

        dunyalar = ["sancak", "yakamoz", "avrasya", "pruva", "velena", "flador", "astra"]
        if dunya_adi in dunyalar:
            await find_and_send_results(message, dunya_adi, x, z, kalan_zaman, claim_sayisi, image_url)
        else:
            await message.channel.send("❌ Geçersiz dünya adı girdin. İşlem iptal edildi.")
    except asyncio.TimeoutError:
        await message.channel.send("⏳ Süre doldu. İşlem iptal edildi.")

async def find_and_send_results(message, dunya_adi, x, z, kalan_zaman, claim_sayisi, image_url):
    hesap_mesafeleri = []

    for hesap in hesaplar.find():
        koordinatlar = hesap["dunyalar"].get(dunya_adi)
        if koordinatlar and "x" in koordinatlar and "z" in koordinatlar:
            hx, hz = koordinatlar["x"], koordinatlar["z"]
            mesafe = math.sqrt((hx - x) ** 2 + (hz - z) ** 2)
            hesap_mesafeleri.append((mesafe, hesap["isim"], (hx, hz)))

    if not hesap_mesafeleri:
        await message.channel.send("❌ Veritabanında bu dünyaya ait hesap bulunamadı.")
        return

    hesap_mesafeleri.sort(key=lambda t: t[0])
    
    embed = discord.Embed(
        title=f"📍 En Yakın Hesaplar ({dunya_adi.capitalize()})",
        color=0x1abc9c
    )
    embed.add_field(name="Aranan Koordinat", value=f"`{x} {z}`", inline=True)
    embed.add_field(name="Kalan Zaman", value=f"`{kalan_zaman}`", inline=True)
    embed.add_field(name="Bölge Sayısı", value=f"`{claim_sayisi}`", inline=True)

    for i, (mesafe, isim, (hx, hz)) in enumerate(hesap_mesafeleri[:2], start=1):
        embed.add_field(
            name=f"{i}. En Yakın Hesap",
            value=f"**{isim}**\nKoordinat: `{hx} {hz}`\nMesafe: `{int(round(mesafe))} blok`",
            inline=False
        )

    embed.set_thumbnail(url=image_url)
    embed.set_footer(
        text=f"Talep eden: {message.author}",
        icon_url=message.author.avatar.url if message.author.avatar else None
    )

    embed.add_field(
        name="⚠️ Önemli",
        value="Ss alırken **Windows + Shift + S** kullanın ve sadece koordinatların olduğu kısmı seçin, aksi takdirde bot okuyamayabilir.",
        inline=False
    )
    await message.channel.send(embed=embed)


bot.run(TOKEN)
