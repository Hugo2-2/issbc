"""
Controlador del editor de texto (MVC - Controller).
Conecta las señales de la vista con las acciones del modelo,
y las señales del modelo con las actualizaciones de la vista.
Integra los diálogos de la práctica 3.
"""

from PyQt5.QtWidgets import (
    QFileDialog, QColorDialog, QFontDialog, QInputDialog
)
from PyQt5.QtCore import Qt, QBasicTimer
from PyQt5.QtGui import QColor, QTextCharFormat, QTextCursor
from pathlib import Path


class EditorController:
    """Controlador que conecta Model y View."""

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self._save_timer = QBasicTimer()
        self._save_step = 0
        self._conectar_signals()

    # =============================
    #  CONEXIÓN DE SEÑALES
    # =============================

    def _conectar_signals(self):
        # --- Señales del modelo → vista ---
        self.model.carpeta_cambiada.connect(self.view.set_carpeta)
        self.model.archivos_actualizados.connect(self.view.set_archivos)
        self.model.archivo_abierto.connect(self._on_archivo_abierto)
        self.model.archivo_guardado.connect(self._on_archivo_guardado)
        self.model.error_ocurrido.connect(self.view.mostrar_error)
        self.model.estado_modificado.connect(self._on_estado_modificado)

        # --- Señales de la vista → controlador ---

        # Botón y acción "Seleccionar carpeta" (file_dialog.py: QFileDialog)
        self.view.btn_seleccionar.clicked.connect(self.seleccionar_carpeta)
        self.view.action_seleccionar.triggered.connect(self.seleccionar_carpeta)

        # Lista de archivos: click para abrir
        self.view.lista_archivos.itemClicked.connect(self._on_archivo_click)

        # Botones guardar (QPushButton: clicked signal)
        self.view.btn_guardar.clicked.connect(self.guardar)
        self.view.btn_guardar_como.clicked.connect(self.guardar_como)
        self.view.action_guardar.triggered.connect(self.guardar)
        self.view.action_guardar_como.triggered.connect(self.guardar_como)

        # Salir
        self.view.action_salir.triggered.connect(self.view.close)

        # Texto modificado → detectar cambios
        self.view.text_edit.textChanged.connect(self._on_texto_cambiado)

        # CheckBox word wrap (check_box.py: stateChanged)
        self.view.cb_word_wrap.stateChanged.connect(self._on_word_wrap)

        # Toggle solo lectura (toggle_button.py: clicked[bool])
        self.view.btn_solo_lectura.clicked[bool].connect(self._on_solo_lectura)

        # Slider tamaño fuente (slider.py: valueChanged[int])
        self.view.font_slider.valueChanged[int].connect(self._on_font_size)

        # Diálogos de formato
        self.view.action_fuente.triggered.connect(self.cambiar_fuente)
        self.view.action_color_texto.triggered.connect(self.cambiar_color_texto)
        self.view.action_color_fondo.triggered.connect(self.cambiar_color_fondo)

        # Buscar y reemplazar (input_dialog.py: QInputDialog)
        self.view.action_buscar.triggered.connect(self.buscar_reemplazar)

    # =============================
    #  CARPETA (file_dialog.py: QFileDialog)
    # =============================

    def seleccionar_carpeta(self):
        home = str(Path.home())
        carpeta = QFileDialog.getExistingDirectory(
            self.view, 'Seleccionar carpeta', home)
        if carpeta:
            self.model.seleccionar_carpeta(carpeta)

    # =============================
    #  ARCHIVOS
    # =============================

    def _on_archivo_click(self, item):
        self.model.abrir_archivo(item.text())

    def _on_archivo_abierto(self, nombre, contenido):
        self.view.set_contenido(contenido)
        self.view.set_titulo(f'{nombre} — Editor de Texto')
        self.view.mostrar_mensaje(f'Abierto: {nombre}')
        self._actualizar_info()

    # =============================
    #  GUARDAR (file_dialog.py: QFileDialog)
    # =============================

    def guardar(self):
        contenido = self.view.get_contenido()
        if self.model.archivo_actual:
            self._animar_guardado()
            self.model.guardar(contenido)
        else:
            self.guardar_como()

    def guardar_como(self):
        home = self.model.carpeta_actual or str(Path.home())
        fname, _ = QFileDialog.getSaveFileName(
            self.view, 'Guardar como', home,
            'Texto (*.txt);;Python (*.py);;Todos (*)')
        if fname:
            contenido = self.view.get_contenido()
            self._animar_guardado()
            self.model.guardar_como(fname, contenido)

    def _on_archivo_guardado(self, nombre):
        self.view.set_titulo(f'{nombre} — Editor de Texto')
        self.view.mostrar_mensaje(f'Guardado: {nombre}')

    # --- Animación de guardado (progressbar.py: QProgressBar + QBasicTimer) ---

    def _animar_guardado(self):
        self._save_step = 0
        self.view.progress_bar.setValue(0)
        self.view.progress_bar.show()
        self._save_timer.start(10, self.view)
        # Guardamos referencia al controller en la vista para el timer
        self.view._ctrl_save_ref = self

    def _tick_progreso(self):
        self._save_step += 5
        self.view.animar_progreso(self._save_step)
        if self._save_step >= 100:
            self._save_timer.stop()

    # =============================
    #  DETECCIÓN DE CAMBIOS
    # =============================

    def _on_texto_cambiado(self):
        contenido = self.view.get_contenido()
        self.model.marcar_modificado(contenido)
        self._actualizar_info()

    def _on_estado_modificado(self, modificado):
        titulo = self.view.windowTitle()
        if modificado and not titulo.startswith('● '):
            self.view.set_titulo(f'● {titulo}')
        elif not modificado and titulo.startswith('● '):
            self.view.set_titulo(titulo[2:])

    def _actualizar_info(self):
        texto = self.view.get_contenido()
        lineas = texto.count('\n') + 1 if texto else 0
        caracteres = len(texto)
        self.view.actualizar_info(lineas, caracteres)

    # =============================
    #  CHECKBOX / TOGGLE (check_box.py, toggle_button.py)
    # =============================

    def _on_word_wrap(self, state):
        """CheckBox ajuste de línea (check_box.py: stateChanged)."""
        if state == Qt.Checked:
            self.view.text_edit.setLineWrapMode(self.view.text_edit.WidgetWidth)
        else:
            self.view.text_edit.setLineWrapMode(self.view.text_edit.NoWrap)

    def _on_solo_lectura(self, checked):
        """Toggle solo lectura (toggle_button.py: QPushButton checkable)."""
        self.view.text_edit.setReadOnly(checked)
        if checked:
            self.view.btn_solo_lectura.setText('Editable')
            self.view.mostrar_mensaje('Modo solo lectura activado')
        else:
            self.view.btn_solo_lectura.setText('Solo lectura')
            self.view.mostrar_mensaje('Modo edición activado')

    # =============================
    #  SLIDER (slider.py: valueChanged[int])
    # =============================

    def _on_font_size(self, value):
        font = self.view.text_edit.font()
        font.setPointSize(value)
        self.view.text_edit.setFont(font)
        self.view.lbl_font_size.setText(str(value))

    # =============================
    #  DIÁLOGOS DE FORMATO
    # =============================

    def cambiar_fuente(self):
        """QFontDialog (font_dialog.py)."""
        font, ok = QFontDialog.getFont(self.view.text_edit.font(), self.view)
        if ok:
            self.view.text_edit.setFont(font)
            self.view.font_slider.setValue(font.pointSize())

    def cambiar_color_texto(self):
        """QColorDialog para texto (color_dialog.py)."""
        color = QColorDialog.getColor(
            self.view.text_edit.textColor(), self.view, 'Color de texto')
        if color.isValid():
            self.view.text_edit.setTextColor(color)
            self.view.mostrar_mensaje(f'Color de texto: {color.name()}')

    def cambiar_color_fondo(self):
        """QColorDialog para fondo (color_dialog.py: QFrame + background)."""
        color = QColorDialog.getColor(
            QColor(255, 255, 255), self.view, 'Color de fondo')
        if color.isValid():
            palette = self.view.text_edit.palette()
            palette.setColor(palette.Base, color)
            self.view.text_edit.setPalette(palette)
            self.view.mostrar_mensaje(f'Color de fondo: {color.name()}')

    # =============================
    #  BUSCAR Y REEMPLAZAR (input_dialog.py: QInputDialog)
    # =============================

    def buscar_reemplazar(self):
        """Usa QInputDialog para buscar y opcionalmente reemplazar texto."""
        buscar, ok = QInputDialog.getText(
            self.view, 'Buscar', 'Texto a buscar:')
        if not ok or not buscar:
            return

        # Buscar y resaltar
        cursor = self.view.text_edit.textCursor()
        cursor.movePosition(QTextCursor.Start)
        self.view.text_edit.setTextCursor(cursor)

        found = self.view.text_edit.find(buscar)
        if not found:
            self.view.mostrar_mensaje(f'No se encontró: "{buscar}"')
            return

        self.view.mostrar_mensaje(f'Encontrado: "{buscar}"')

        # Preguntar si quiere reemplazar
        reemplazo, ok2 = QInputDialog.getText(
            self.view, 'Reemplazar',
            f'Reemplazar "{buscar}" por (vacío para cancelar):')
        if ok2 and reemplazo:
            texto = self.view.get_contenido()
            count = texto.count(buscar)
            nuevo = texto.replace(buscar, reemplazo)
            self.view.set_contenido(nuevo)
            self.view.mostrar_mensaje(
                f'Reemplazadas {count} ocurrencias de "{buscar}"')
