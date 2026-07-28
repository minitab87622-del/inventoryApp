[app]

title = المخزون الحالي

package.name = inventoryapp

package.domain = org.odey

source.dir = .

source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,json,db

version = 1.0

requirements = python3,kivy==2.3.1,arabic-reshaper

orientation = portrait

fullscreen = 0

icon.filename = icon.png

presplash.filename = background.png

android.permissions = INTERNET

android.api = 33

android.minapi = 21

android.ndk = 25b

android.archs = arm64-v8a,armeabi-v7a

android.allow_backup = True

android.accept_sdk_license = True

log_level = 2

warn_on_root = 1

#

# لا تعدل ما تحت إلا إذا احتجت

#

[buildozer]

log_level = 2

warn_on_root = 1
