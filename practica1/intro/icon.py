#!/usr/bin/python

"""
ZetCode PyQt5 tutorial

This example shows an icon
in the titlebar of the window.

Author: Jan Bodnar
Website: zetcode.com
"""

import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.setGeometry(500, 300, 600, 400)
        self.setWindowTitle('Icon')
        icon_path = Path(__file__).resolve().parent / 'square-arrow-right-exit.png'
        icon = QIcon(str(icon_path))
        self.setWindowIcon(icon)
        QApplication.setWindowIcon(icon)

        self.show()


def main():

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
