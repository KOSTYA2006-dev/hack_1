import sys
from PyQt5.QtWidgets import QApplication, QWidget


def move2RightBottomCorner(win):
    screen_geometry = QApplication.desktop().availableGeometry()
    screen_size = (screen_geometry.width(), screen_geometry.height())
    win_size = (win.frameSize().width(), win.frameSize().height())
    x = screen_size[0] - win_size[0]
    y = screen_size[1] - win_size[1]
    win.move(x, y)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QWidget()
    w.move(w.width() * -3, 0) # чтобы не мелькало
    w.show()
    move2RightBottomCorner(w)
    sys.exit(app.exec_())