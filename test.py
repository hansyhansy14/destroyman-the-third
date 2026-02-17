import sys
from PyQt6 import QtWidgets, QtGui, QtCore
import random
window = None
label = None
sprite = None
is_squished = False  # toggle state


anchor_y = 1080  # bottom of the character when standing
anchor_x = 1700  # all the way on the righthand side essentially
def bob_squish():
    global is_squished, sprite, window, anchor_x, anchor_y

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

    # move window so bottom stays at anchor_y, X stays fixed
    window.move(anchor_x, anchor_y - height)

    # update label
    label.setPixmap(squished_pixmap)


def spawn_text():
    # Create a label for text
    text_label = QtWidgets.QLabel(window)
    text_label.setText("hello! i am a placeholder!")  # < will be able to choose from a dictionary of speeches (will be toggleable! TODO)
    text_label.setStyleSheet(
        "background-color: yellow; border: 2px solid black; padding: 5px;")
    text_label.adjustSize()
    text_label.move(0, -50)  # position slightly to the left upward from the character
    text_label.show()

app = QtWidgets.QApplication(sys.argv)

# create main "window"
window = QtWidgets.QWidget()
window.setWindowFlags(
    QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint | QtCore.Qt.WindowType.WindowTransparentForInput)
window.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
window.setWindowTitle(":3")
window.setFixedSize(200, 200)

# load sprite for the first time (gonna bug out a little, but reset into "standardized" (not normalized; standard = 1920x1080p res) position after 1sec)
sprite = QtGui.QPixmap(r".\resources\diii_normal.png")

# label to show sprite
label = QtWidgets.QLabel(window)
label.setPixmap(sprite)
label.setFixedSize(200, 200)
label.show()

# Initial window position
window.move(400, 300)
window.show()

# squish timer
bob_timer = QtCore.QTimer()
bob_timer.timeout.connect(bob_squish)
bob_timer.start(1000)  # 1sec

# text timer (NON FUNCTIONAL AS OF NOW; TODO)
QtCore.QTimer.singleShot(5000, spawn_text)

# ---------------- Run --------------------------
sys.exit(app.exec())
