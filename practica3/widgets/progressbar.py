from PyQt5.QtWidgets import (QWidget, QProgressBar,
                             QPushButton, QApplication, QVBoxLayout)
from PyQt5.QtCore import QBasicTimer
import sys


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.pbar = QProgressBar(self)
        self.pbar.setMinimum(0)
        self.pbar.setMaximum(100)
        self.pbar.setValue(0)
        self.pbar.setTextVisible(True)

        self.btn = QPushButton('Start', self)
        self.btn.clicked.connect(self.doAction)

        vbox = QVBoxLayout()
        vbox.addWidget(self.pbar)
        vbox.addWidget(self.btn)
        self.setLayout(vbox)

        self.timer = QBasicTimer()
        self.step = 0

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('QProgressBar')
        self.show()

    def timerEvent(self, e):

        if self.step >= 100:
            self.timer.stop()
            self.btn.setText('Finished')
            return

        self.step = self.step + 1
        self.pbar.setValue(self.step)

    def doAction(self):

        if self.timer.isActive():
            self.timer.stop()
            self.btn.setText('Start')
        else:
            self.timer.start(100, self)
            self.btn.setText('Stop')


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
