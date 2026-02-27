import sys
from PyQt6 import QtWidgets, QtGui, QtCore
import random
import os
import sys
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import requests
import pygame as pg

# todo: toggle_sounds
# def toggle_sounds():

# discord https://www.youtube.com/watch?v=vKyK6CAnjdc
# typing www.youtube.com/watch?v=sqge5keBCq4&pp=ygUTa2V5Ym9hcmQgdHlwaW5nIHNmeA%3D%3D
# golf hi1 wii sports https://www.youtube.com/watch?v=HqGCHBiz-jY
# kid making robot sounds https://www.youtube.com/watch?v=kIJNOhXRQNE (boop)
# whatsapp whistle https://www.youtube.com/watch?v=SXXVS1RpoMI
# fnaf kids cheering www.youtube.com/watch?v=9bnUWuAO0oU&pp=ygUTZm5hZiA0IGtpZHMgeWF5IHNmeA%3D%3D (for default)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def get_speeches(url):
    try:
        response = requests.get(url,timeout=5)
        response.raise_for_status()
        lines = [line.strip() for line in response.text.splitlines() if line.strip()]
        return lines
    except Exception as e:
        print("failed to fetch speeches.txt: ",e)
        return None

pg.mixer.init()
discord_ping = pg.mixer.Sound(dp_path)
whatsapp_notification = pg.mixer.Sound(wn_path)
roar = pg.mixer.Sound(roar_path)
beep = pg.mixer.Sound(boop)
roar2 = pg.mixer.Sound(roar2_path)
typing = pg.mixer.Sound(typing_path)
putter = pg.mixer.Sound(putter_path)
default = pg.mixer.Sound(kc_path)

kc_path = 
putter_path = 
typing_path = 
roar2_path = 
boop = 
roar_path = 
wn_path = 
dp_path = 
sprite_size = (200,200)
window = None
label = None
sprite = None
is_squished = False  # toggle state
url = "https://raw.githubusercontent.com/hansyhansy14/destroyman-the-third/main/dist/resources/speeches.txt"
skin_index = 0
skins = [
    "resources/skins/diii_normal.png",
    "resources/skins/diii_evil.png",
    "resources/skins/diii_whatsapp.png",
    "resources/skins/diii_discord.png",
    "resources/skins/diii_golf.png",
    "resources/skins/diii_linux.png",
    "resources/skins/diii_monster.png",
    "resources/skins/diii_cisco.png"

]
# normalized position ratios (0–1)
anchor_x_ratio = 1.0  # 100% across screen width (right-hand side)
anchor_y_ratio = 0.13  # 0% (top)

def normalized_pixmap(path):
    pixmap = QtGui.QPixmap(path)
    return pixmap.scaled(
        sprite_size[0],
        sprite_size[1],
        QtCore.Qt.AspectRatioMode.IgnoreAspectRatio,
        QtCore.Qt.TransformationMode.SmoothTransformation
    )

def cycle_back(icon=None,item=None):
    global skin_index, sprite
    skin_index = (skin_index-1) % len(skins)
    new_path = resource_path(skins[skin_index])
    sprite=normalized_pixmap(new_path)
    if skin_index == 0:
        pg.mixer.Sound.play(default)
    elif skin_index == 1:    
        pg.mixer.Sound.play(roar)
    elif skin_index == 2: 
        pg.mixer.Sound.play(whatsapp_notification)
    elif skin_index == 3:
        pg.mixer.Sound.play(discord_ping)
    elif skin_index == 4:
        pg.mixer.Sound.play(putter)
    elif skin_index == 5:
        pg.mixer.Sound.play(typing)
    elif skin_index == 6:
        pg.mixer.Sound.play(roar2)
    elif skin_index == 7:
        pg.mixer.Sound.play(beep)
        
    # redraws sprite on next bob
    bob_squish()

def cycle_forth(icon=None,item=None):
    global skin_index, sprite
    skin_index = (skin_index+1) % len(skins)
    new_path = resource_path(skins[skin_index])
    sprite=normalized_pixmap(new_path)
    # redraws sprite on next bob
    bob_squish()

def bob_squish():
    global is_squished, sprite, window, label

    # toggle squish state
    is_squished = not is_squished

    # calculate new height
    width = 200
    height = 200 if not is_squished else 190  # squish height

    # rescale the sprite
    squished_pixmap = sprite.scaled(
        width, height,
        QtCore.Qt.AspectRatioMode.IgnoreAspectRatio,
        QtCore.Qt.TransformationMode.SmoothTransformation
    )

    # dynamically calculate anchor position based on screen size
    screen = app.primaryScreen()
    screen_geom = screen.geometry()
    screen_width = screen_geom.width()
    screen_height = screen_geom.height()

    anchor_x = int(screen_width * anchor_x_ratio) - window.width()
    anchor_y = int(screen_height * anchor_y_ratio)

    # move window so bottom stays at anchor_y
    window.move(anchor_x, anchor_y - height)

    # update label
    label.setPixmap(squished_pixmap)


def load_speeches(path):
    with open(path, 'r', encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
        return lines

speeches = get_speeches(url) # gets speeches.txt from github page first and foremost
if not speeches:
    speeches = load_speeches(resource_path("resources/speeches.txt")) # fallback in case user has no internet


first_message_shown = False

def spawn_text():
    global first_message_shown

    text_label = QtWidgets.QLabel(window)

    if not first_message_shown:
        # hardcoded first message
        text_label.setText("Thank you for contracting [ CORAL FEVER ]! I'm your new personal assistant, Destroyman III. I'll be your right hand - your emotional support buddy.")  # <-- your custom first message
        first_message_shown = True
    elif speeches:
        text_label.setText(random.choice(speeches))
    else:
        text_label.setText("...")

    text_label.setStyleSheet(
        "background-color: lightgrey; " 
        "border: 2px solid black; " 
        "padding: 5px;"
        "color: black;"
    )
    text_label.setWordWrap(True)

    max_width = window.width() - 20
    text_label.setMaximumWidth(max_width)

    # start with normal font size
    font_size = 14
    text_label.setFont(QtGui.QFont(fondamento_family, font_size))
    text_label.adjustSize()

    delta = 70 # pixels below sprite

    # shrink font if text exceeds space below sprite
    available_space = window.height() - label.height() - delta
    while text_label.height() > available_space and font_size > 6:
        font_size -= 1
        text_label.setFont(QtGui.QFont(fondamento_family, font_size))
        text_label.adjustSize()

    # horizontally center
    x = (window.width() - text_label.width()) // 2
    # vertically float below sprite
    y = window.height() - label.height() + delta - text_label.height()

    text_label.move(x, y)
    text_label.show()

    # auto-remove after 10 sec
    QtCore.QTimer.singleShot(10000, text_label.deleteLater)

    # schedule next speech
    delay = random.randint(20000, 30000)
    QtCore.QTimer.singleShot(delay, spawn_text)



app = QtWidgets.QApplication(sys.argv)

def quit_app(icon, item):
    icon.stop()
    QtCore.QTimer.singleShot(0, app.quit)

base_dir = os.path.dirname(os.path.abspath(__file__))
font_path = resource_path("resources/fonts/Fondamento-Regular.ttf")
font_id = QtGui.QFontDatabase.addApplicationFont(font_path)

if font_id == -1:
    print("failed to load fondamento")
    fondamento_family = "Arial"  # fallback if fondamento not found for some reason
else:
    families = QtGui.QFontDatabase.applicationFontFamilies(font_id)
    fondamento_family = families[0]
    print("loaded font family:", fondamento_family)

font = QtGui.QFont(fondamento_family, 14)

# create main "window"
window = QtWidgets.QWidget()
window.setWindowFlags(
    QtCore.Qt.WindowType.FramelessWindowHint | 
    QtCore.Qt.WindowType.WindowStaysOnTopHint | 
    QtCore.Qt.WindowType.Tool |
    QtCore.Qt.WindowType.WindowTransparentForInput
)
window.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
window.setWindowTitle(":3")
window.setFixedSize(200, 400)

# load sprite
sprite = normalized_pixmap(resource_path(skins[skin_index]))

# label to show sprite
label = QtWidgets.QLabel(window)
label.setPixmap(sprite)
label.setFixedSize(200, 200)
label.show()

# initial window position: call bob_squish once to normalize for current screen
bob_squish()

window.show()
window.raise_()
window.activateWindow()

def create_tray_icon():
    # create a simple icon image (or load yours)
    image = Image.open(resource_path("resources/destroy.ico"))

    menu = Menu(
        MenuItem("Quit", quit_app),
        MenuItem("Change Skin (Cycle Forward)",cycle_forth),
        MenuItem("Change Skin (Cycle Back)",cycle_back)
        #MenuItem("Toggle Sounds", toggle_sounds)
    )

    icon = Icon("destroyman", image, "Destroyman III", menu)
    icon.run_detached()
    return icon

tray_icon = create_tray_icon()

# squish timer
bob_timer = QtCore.QTimer()
bob_timer.timeout.connect(bob_squish)
bob_timer.start(1000)  # 1sec

# text timer
QtCore.QTimer.singleShot(5000, spawn_text)

sys.exit(app.exec())