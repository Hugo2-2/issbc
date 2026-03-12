#!/usr/python
"""
ZetCode PytQt5 tutorial

In this example we create a simple
window in PyQt5.

Author: Hugo Espejo
Website: zetcode.com
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget

def main():

    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(600, 400)
    w.move(500, 300)
    w.setWindowTitle('Hola Mundo')
    w.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()