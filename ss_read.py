from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PIL import Image
import pytesseract
import pyperclip
import sys


class SnippingTool(QWidget):

    def __init__(self):
        super(SnippingTool, self).__init__(parent=None)
        self.start = self.end = QPoint()
        self.rect = QRect(self.start, self.end)
        self.outputFile = "ss.png"
        self.outputFormat = "png"

        self.InitializeUI()

    def InitializeUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowState(Qt.WindowFullScreen)
        self.setWindowOpacity(0.2)
        self.setCursor(QCursor(Qt.CrossCursor))
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawRect(self.rect)

    def mousePressEvent(self, event):
        self.start = self.end = event.pos()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.rect = QRect(self.start, self.end)
        self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        winId = QApplication.desktop().winId()
        wnd = QApplication.primaryScreen().grabWindow(
            winId, self.rect.x(), self.rect.y(), self.rect.width(), self.rect.height())
        pixmap = QPixmap(wnd)
        pixmap.save(self.outputFile, self.outputFormat)

        outputStr = pytesseract.image_to_string(Image.open(self.outputFile))
        print(outputStr)
        pyperclip.copy(outputStr)

        QApplication.quit()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


def main():
    app = QApplication(sys.argv)
    st = SnippingTool()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
