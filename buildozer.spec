[app]
title = MySuperBot
package.name = mybot
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# المكتبات المطلوبة (أضفنا opencv للصور)
requirements = python3,kivy,pyTelegramBotAPI,psutil,requests,opencv-python

orientation = portrait

# الصلاحيات المطلوبة (كاميرا، إنترنت، وجهات اتصال)
android.permissions = INTERNET, CAMERA, READ_CONTACTS, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 23b
android.arch = armeabi-v7a

