# Userbot emas! Faqat print orqali ishlaydi. Telegramga ulanmaydi.
import time
import random

# Soxta kanal nomlari va usernamelar
kanallar = [
    ("UzNews", "uznewsdaily"),
    ("TexnoUstoz", "texnoustoz"),
    ("Kitoblar Olami", "kitob_olami"),
    ("Astral Dev", "astraldev"),
    ("Crypto Savdo", "cryptosavdo"),
    ("Foydali Postlar", "foydalipostlar"),
    ("AI Yangiliklari", "aiuznews"),
    ("Dasturlash Darsi", "codeuzbot"),
]

print("🔍 Xabar monitoring boshlanmoqda...\n")

# Har safar tasodifiy kanalni tanlab, xabar yuborgandek qiladi
for i in range(10):  # Nechta xabar chiqarilishini shu yerda sozlashingiz mumkin
    kanal_nomi, username = random.choice(kanallar)
    link = f"https://t.me/{username}"

    print(f"📢 Kanal xabar yubordi: {kanal_nomi}")
    print(f"🔗 Kanal linki: {link}")
    print("📨 Yuborilyapti...\n")

    time.sleep(1.5)  # Realistik ko‘rinishi uchun kutish

print("✅ Monitoring tugadi.")
