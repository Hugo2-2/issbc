#!/usr/bin/python

"""
Ejercicio Final – Práctica I (ISSBC)
======================================
Ventana PyQt5 que reúne los elementos vistos en intro/ y avanzado/:

  - Ventana básica con título y geometría        (simple.py)
  - Centrado en pantalla                         (center.py)
  - Diálogo de confirmación al cerrar            (messagebox.py)
  - Botón Salir                                  (quit_button.py)
  - Tooltips en widgets                          (tooltip.py)
  - Barra de estado                              (status.py)
  - Menú con acción Salir y atajo Ctrl+Q         (simple_menu.py)
  - Submenú anidado                              (submenu.py)
  - Acción checkable (muestra/oculta statusbar)  (check_menu.py)
  - Menú contextual con clic derecho             (context_menu.py)
  - Barra de herramientas                        (toolbar.py)
  - QMainWindow con widget central               (main_window.py)
"""

import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QAction, QMenu,
    QTextEdit, QMessageBox, QPushButton,
    QVBoxLayout, QWidget, QToolTip, QDesktopWidget
)
from PyQt5.QtGui import QFont


class EjercicioFinal(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # ── Tooltip global (tooltip.py) ───────────────────────────────
        QToolTip.setFont(QFont('SansSerif', 10))

        # ── Widget central: editor + botón (main_window.py, quit_button.py) ──
        textEdit = QTextEdit()
        textEdit.setToolTip('Editor de texto')          # tooltip.py

        quitBtn = QPushButton('Salir')
        quitBtn.setToolTip('Cierra la aplicación')      # tooltip.py
        quitBtn.clicked.connect(self.close)             # quit_button.py

        layout = QVBoxLayout()
        layout.addWidget(textEdit)
        layout.addWidget(quitBtn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)                # main_window.py

        # ── Barra de estado (status.py) ───────────────────────────────
        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Listo')

        # ── Barra de menús ────────────────────────────────────────────
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)

        # Menú Archivo (simple_menu.py)
        fileMenu = menubar.addMenu('&Archivo')

        # Submenú Importar (submenu.py)
        importMenu = QMenu('Importar', self)
        importMenu.addAction('Importar correo')
        importMenu.addAction('Importar archivo')
        fileMenu.addMenu(importMenu)

        fileMenu.addSeparator()

        # Acción Salir con atajo de teclado (simple_menu.py)
        exitAct = QAction('&Salir', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Cierra la aplicación')
        exitAct.triggered.connect(self.close)
        fileMenu.addAction(exitAct)

        # Menú Vista – acción checkable (check_menu.py)
        viewMenu = menubar.addMenu('&Vista')
        viewStatAct = QAction('Mostrar barra de estado', self, checkable=True)
        viewStatAct.setChecked(True)
        viewStatAct.triggered.connect(self.toggleStatusbar)
        viewMenu.addAction(viewStatAct)

        # ── Barra de herramientas (toolbar.py) ────────────────────────
        toolbar = self.addToolBar('Principal')
        toolbar.addAction(exitAct)                      # reutiliza la acción Salir

        # ── Propiedades de la ventana (simple.py) ─────────────────────
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('Ejercicio Final – PyQt5')
        self.setToolTip('Ventana principal')

        # Centrar en pantalla (center.py)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self.show()

    def toggleStatusbar(self, state):
        """Muestra u oculta la barra de estado (check_menu.py)."""
        if state:
            self.statusbar.show()
        else:
            self.statusbar.hide()

    def contextMenuEvent(self, event):
        """Menú contextual al hacer clic derecho (context_menu.py)."""
        cmenu = QMenu(self)
        cmenu.addAction('Nuevo')
        quitAct = cmenu.addAction('Salir')
        action = cmenu.exec_(self.mapToGlobal(event.pos()))
        if action == quitAct:
            self.close()

    def closeEvent(self, event):
        """Pide confirmación antes de cerrar (messagebox.py)."""
        reply = QMessageBox.question(
            self, 'Salir', '¿Seguro que quieres salir?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


def main():
    app = QApplication(sys.argv)
    ex = EjercicioFinal()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
