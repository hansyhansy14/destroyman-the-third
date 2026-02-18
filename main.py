import sys
from PyQt6 import QtWidgets, QtGui, QtCore
import random
import os

window = None
label = None
sprite = None
is_squished = False  # toggle state

# normalized position ratios (0–1)
anchor_x_ratio = 1.0  # 100% across screen width (right-hand side)
anchor_y_ratio = 0.13  # 0% (top)

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

    # dynamically calculate anchor position based on screen size (chatgpt made this one :,/ )
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

speeches = load_speeches("speeches.txt")


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
        "background-color: yellow; border: 2px solid black; padding: 5px;"
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

base_dir = os.path.dirname(os.path.abspath(__file__))
font_path = os.path.join(base_dir, "resources", "fonts", "Fondamento-Regular.ttf")
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
    QtCore.Qt.WindowType.WindowTransparentForInput
)
window.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
window.setWindowTitle(":3")
window.setFixedSize(200, 400)

# load sprite
sprite = QtGui.QPixmap(r".\resources\diii_normal.png")

# label to show sprite
label = QtWidgets.QLabel(window)
label.setPixmap(sprite)
label.setFixedSize(200, 200)
label.show()

# Initial window position: call bob_squish once to normalize for current screen
bob_squish()

window.show()

# squish timer
bob_timer = QtCore.QTimer()
bob_timer.timeout.connect(bob_squish)
bob_timer.start(1000)  # 1sec

# text timer
QtCore.QTimer.singleShot(5000, spawn_text)

sys.exit(app.exec())