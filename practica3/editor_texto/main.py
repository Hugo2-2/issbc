"""
Editor de Texto — Práctica 3 ISSBC
Punto de entrada. Instancia Model, View y Controller (patrón MVC).
"""

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QBasicTimer
import sys

from model import EditorModel
from view import EditorView
from controller import EditorController


class App:
    """Clase que ensambla el patrón MVC y gestiona el timer de progreso."""

    def __init__(self):
        self.model = EditorModel()
        self.view = EditorView()
        self.controller = EditorController(self.model, self.view)

        # Sobreescribimos timerEvent de la vista para manejar
        # tanto el reloj como la animación de guardado
        original_timer = self.view.timerEvent
        ctrl = self.controller

        def custom_timer(e):
            if hasattr(ctrl, '_save_timer') and ctrl._save_timer.isActive():
                ctrl._tick_progreso()
            original_timer(e)

        self.view.timerEvent = custom_timer
        self.view.show()


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    editor = App()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
