#!/usr/bin/python

"""
Editor de Texto – Práctica II (ISSBC)
======================================
Editor de ficheros .txt en PyQt5 que integra todos los elementos vistos
en las carpetas 'intro' y 'avanzado'.

La aplicación trabaja exclusivamente con ficheros de texto plano (.txt)
y ofrece las operaciones: Nuevo, Abrir, Guardar y Guardar como.

Elementos integrados:

  [intro]
  -------
  · simple.py      → ventana básica, título, geometría
  · center.py      → centrado en pantalla con QDesktopWidget
  · icon.py        → icono en la barra de título (QIcon)
  · messagebox.py  → diálogo de confirmación al cerrar (closeEvent)
  · quit_button.py → botón conectado a close()
  · tooltip.py     → QToolTip y setToolTip en widgets

  [avanzado]
  ----------
  · status.py      → barra de estado con showMessage
  · simple_menu.py → barra de menús, QAction, atajo de teclado
  · submenu.py     → submenú anidado (QMenu dentro de otro QMenu)
  · check_menu.py  → acción checkable que activa/desactiva un widget
  · context_menu.py→ menú contextual con contextMenuEvent
  · toolbar.py     → barra de herramientas con QAction
  · main_window.py → QMainWindow con menubar + toolbar + statusbar + central widget
"""

import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QAction, QMenu,
    QTextEdit, QMessageBox, QPushButton, QFileDialog,
    QVBoxLayout, QWidget, QToolTip, QDesktopWidget
)
from PyQt5.QtGui import QIcon, QFont


class EjercicioFinal(QMainWindow):
    """
    Ventana principal de la aplicación.
    Hereda de QMainWindow (main_window.py) para disponer de
    menubar, toolbar y statusbar de forma nativa.
    """

    def __init__(self):
        super().__init__()
        self.current_file = None   # Ruta del fichero .txt abierto/guardado
        self.initUI()

    # ──────────────────────────────────────────────────────────────────
    # Construcción de la interfaz
    # ──────────────────────────────────────────────────────────────────

    def initUI(self):
        """Inicializa y ensambla todos los componentes de la interfaz."""

        # Fuente global para los tooltips (tooltip.py)
        QToolTip.setFont(QFont('Sans Serif', 10))

        # Widget central con editor y botón (main_window.py + quit_button.py)
        self._build_central_widget()

        # Barra de menús completa (simple_menu.py + submenu.py + check_menu.py)
        self._build_menubar()

        # Barra de herramientas (toolbar.py + main_window.py)
        self._build_toolbar()

        # Barra de estado (status.py + main_window.py)
        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Listo')

        # Título y tamaño inicial (simple.py)
        self.setGeometry(300, 300, 750, 520)
        self.setWindowTitle('Ejercicio Final – PyQt5')

        # Tooltip sobre la propia ventana (tooltip.py)
        self.setToolTip('Ventana principal de la aplicación')

        # Centrar en pantalla (center.py)
        self._center()

        self.show()

    def _build_central_widget(self):
        """
        Crea el widget central compuesto por:
          · QTextEdit  → área de texto editable (main_window.py)
          · QPushButton → botón 'Salir' con tooltip (quit_button.py + tooltip.py)
        """
        container = QWidget()
        layout = QVBoxLayout()

        # Editor de texto (main_window.py)
        self.textEdit = QTextEdit()
        self.textEdit.setPlaceholderText('Escribe algo aquí...')
        self.textEdit.setToolTip('Editor de texto principal')   # tooltip.py
        layout.addWidget(self.textEdit)

        # Botón de salida con tooltip (quit_button.py + tooltip.py)
        quitBtn = QPushButton('Salir')
        quitBtn.setToolTip('Cierra la aplicación')              # tooltip.py
        quitBtn.setFixedHeight(32)
        quitBtn.clicked.connect(self.close)                     # quit_button.py
        layout.addWidget(quitBtn)

        container.setLayout(layout)
        self.setCentralWidget(container)

    def _build_menubar(self):
        """
        Construye la barra de menús con tres menús:

          Archivo → Nuevo | Abrir | Guardar | Guardar como | --- | Salir
          Vista   → [✓] Mostrar barra de estado | [✓] Mostrar barra de herramientas
          Ayuda   → Acerca de

        La aplicación trabaja exclusivamente con ficheros .txt.
        """
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)   # Fuerza el menú dentro de la ventana

        # ── Menú Archivo ─────────────────────────────────────────────
        fileMenu = menubar.addMenu('&Archivo')

        # Acción Nuevo
        newAct = QAction('&Nuevo', self)
        newAct.setShortcut('Ctrl+N')
        newAct.setStatusTip('Crea un nuevo documento')
        newAct.triggered.connect(self._on_new)
        fileMenu.addAction(newAct)

        # Acción Abrir fichero .txt
        openAct = QAction('&Abrir', self)
        openAct.setShortcut('Ctrl+O')
        openAct.setStatusTip('Abre un fichero de texto (.txt)')
        openAct.triggered.connect(self._on_open)
        fileMenu.addAction(openAct)

        fileMenu.addSeparator()

        # Acción Guardar
        saveAct = QAction('&Guardar', self)
        saveAct.setShortcut('Ctrl+S')
        saveAct.setStatusTip('Guarda el fichero actual')
        saveAct.triggered.connect(self._on_save)
        fileMenu.addAction(saveAct)

        # Acción Guardar como
        saveAsAct = QAction('Guardar &como...', self)
        saveAsAct.setShortcut('Ctrl+Shift+S')
        saveAsAct.setStatusTip('Guarda el fichero en una nueva ubicación')
        saveAsAct.triggered.connect(self._on_save_as)
        fileMenu.addAction(saveAsAct)

        fileMenu.addSeparator()

        # Acción Salir con atajo de teclado (simple_menu.py + toolbar.py)
        exitAct = QAction('&Salir', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Cierra la aplicación')
        exitAct.triggered.connect(self.close)
        fileMenu.addAction(exitAct)
        self.exitAct = exitAct              # se reutiliza en la toolbar

        # ── Menú Vista (check_menu.py) ────────────────────────────────
        viewMenu = menubar.addMenu('&Vista')

        # Toggle barra de estado – checkable (check_menu.py)
        self.viewStatAct = QAction('Mostrar barra de estado', self, checkable=True)
        self.viewStatAct.setChecked(True)
        self.viewStatAct.setStatusTip('Muestra u oculta la barra de estado')
        self.viewStatAct.triggered.connect(self._toggle_statusbar)
        viewMenu.addAction(self.viewStatAct)

        # Toggle barra de herramientas – checkable (extensión de check_menu.py)
        self.viewToolAct = QAction('Mostrar barra de herramientas', self, checkable=True)
        self.viewToolAct.setChecked(True)
        self.viewToolAct.setStatusTip('Muestra u oculta la barra de herramientas')
        self.viewToolAct.triggered.connect(self._toggle_toolbar)
        viewMenu.addAction(self.viewToolAct)

        # ── Menú Ayuda ────────────────────────────────────────────────
        helpMenu = menubar.addMenu('A&yuda')

        aboutAct = QAction('&Acerca de', self)
        aboutAct.setStatusTip('Información sobre la aplicación')
        aboutAct.triggered.connect(self._show_about)
        helpMenu.addAction(aboutAct)

    def _build_toolbar(self):
        """
        Crea la barra de herramientas con acciones de uso frecuente.
        Basado en toolbar.py y main_window.py.
        """
        self.toolbar = self.addToolBar('Principal')

        newToolAct = QAction('Nuevo', self)
        newToolAct.setStatusTip('Nuevo documento')
        newToolAct.triggered.connect(self._on_new)
        self.toolbar.addAction(newToolAct)

        openToolAct = QAction('Abrir', self)
        openToolAct.setStatusTip('Abre un fichero .txt')
        openToolAct.triggered.connect(self._on_open)
        self.toolbar.addAction(openToolAct)

        saveToolAct = QAction('Guardar', self)
        saveToolAct.setStatusTip('Guarda el fichero actual')
        saveToolAct.triggered.connect(self._on_save)
        self.toolbar.addAction(saveToolAct)

        saveAsToolAct = QAction('Guardar como', self)
        saveAsToolAct.setStatusTip('Guarda el fichero en una nueva ubicación')
        saveAsToolAct.triggered.connect(self._on_save_as)
        self.toolbar.addAction(saveAsToolAct)

        self.toolbar.addSeparator()

        # Reutiliza la acción Salir definida en el menú (toolbar.py)
        self.toolbar.addAction(self.exitAct)

    # ──────────────────────────────────────────────────────────────────
    # Slots y métodos auxiliares
    # ──────────────────────────────────────────────────────────────────

    def _center(self):
        """
        Centra la ventana en la pantalla disponible.
        Tomado directamente de center.py.
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _on_new(self):
        """Limpia el editor y actualiza la barra de estado."""
        self.textEdit.clear()
        self.current_file = None
        self.statusbar.showMessage('Nuevo documento creado')    # status.py

    def _on_open(self):
        """Abre un fichero .txt y carga su contenido en el editor."""
        filepath, _ = QFileDialog.getOpenFileName(
            self, 'Abrir fichero de texto', '',
            'Archivos de texto (*.txt)'
        )
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    self.textEdit.setText(f.read())
                self.current_file = filepath
                self.statusbar.showMessage(f'Abierto: {filepath}')
            except Exception as e:
                QMessageBox.warning(self, 'Error al abrir', str(e))

    def _on_save(self):
        """
        Guarda el contenido del editor.
        Si el fichero ya existe (fue abierto o guardado previamente),
        se sobrescribe en la misma ruta. Si no, delega en Guardar como.
        """
        if self.current_file:
            try:
                with open(self.current_file, 'w', encoding='utf-8') as f:
                    f.write(self.textEdit.toPlainText())
                self.statusbar.showMessage(f'Guardado: {self.current_file}')
            except Exception as e:
                QMessageBox.warning(self, 'Error al guardar', str(e))
        else:
            self._on_save_as()

    def _on_save_as(self):
        """Permite elegir la ubicación y nombre para guardar el fichero .txt."""
        filepath, _ = QFileDialog.getSaveFileName(
            self, 'Guardar como', '',
            'Archivos de texto (*.txt)'
        )
        if filepath:
            if not filepath.endswith('.txt'):
                filepath += '.txt'
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(self.textEdit.toPlainText())
                self.current_file = filepath
                self.statusbar.showMessage(f'Guardado: {filepath}')
            except Exception as e:
                QMessageBox.warning(self, 'Error al guardar', str(e))

    def _toggle_statusbar(self, state):
        """
        Muestra u oculta la barra de estado según el estado del check.
        Lógica extraída de check_menu.py → toggleMenu().
        """
        if state:
            self.statusbar.show()
        else:
            self.statusbar.hide()

    def _toggle_toolbar(self, state):
        """
        Muestra u oculta la barra de herramientas.
        Aplica el mismo patrón que _toggle_statusbar (check_menu.py).
        """
        if state:
            self.toolbar.show()
        else:
            self.toolbar.hide()

    def _show_about(self):
        """
        Muestra un cuadro de información sobre la aplicación.
        Usa QMessageBox (messagebox.py).
        """
        QMessageBox.information(
            self,
            'Acerca de',
            '<b>Ejercicio Final – PyQt5</b><br>'
            'Práctica I – ISSBC<br><br>'
            'Interfaz que integra todos los conceptos vistos en<br>'
            'las carpetas <i>intro</i> y <i>avanzado</i>.'
        )

    def contextMenuEvent(self, event):
        """
        Muestra un menú contextual al hacer clic derecho sobre la ventana.
        Basado en context_menu.py.
        """
        cmenu = QMenu(self)

        newAct     = cmenu.addAction('Nuevo')
        openAct    = cmenu.addAction('Abrir')
        saveAct    = cmenu.addAction('Guardar')
        saveAsAct  = cmenu.addAction('Guardar como')
        cmenu.addSeparator()
        clearAct = cmenu.addAction('Limpiar editor')
        cmenu.addSeparator()
        aboutAct = cmenu.addAction('Acerca de')
        cmenu.addSeparator()
        quitAct  = cmenu.addAction('Salir')

        # Muestra el menú en la posición del cursor (context_menu.py)
        action = cmenu.exec_(self.mapToGlobal(event.pos()))

        if action == newAct:
            self._on_new()
        elif action == openAct:
            self._on_open()
        elif action == saveAct:
            self._on_save()
        elif action == saveAsAct:
            self._on_save_as()
        elif action == clearAct:
            self.textEdit.clear()
        elif action == aboutAct:
            self._show_about()
        elif action == quitAct:
            self.close()

    def closeEvent(self, event):
        """
        Intercepta el evento de cierre y pide confirmación al usuario.
        Tomado de messagebox.py y center.py (closeEvent).
        """
        reply = QMessageBox.question(
            self,
            'Confirmar salida',
            '¿Seguro que quieres cerrar la aplicación?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No                                      # opción por defecto
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


# ──────────────────────────────────────────────────────────────────────
# Punto de entrada
# ──────────────────────────────────────────────────────────────────────

def main():
    app = QApplication(sys.argv)
    ex = EjercicioFinal()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
