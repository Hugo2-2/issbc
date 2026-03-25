"""
Vista del editor de texto (MVC - View).
Construye toda la interfaz gráfica siguiendo el layout de la imagen,
integrando los elementos de la práctica 3.
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QAction, QLabel, QLineEdit, QTextEdit,
    QPushButton, QListWidget, QFrame, QCheckBox, QSlider, QProgressBar,
    QVBoxLayout, QHBoxLayout, QSplitter, QStatusBar, QSizePolicy
)
from PyQt5.QtCore import Qt, QBasicTimer
from PyQt5.QtGui import QFont, QColor


class EditorView(QMainWindow):
    """Vista principal del editor de texto."""

    def __init__(self):
        super().__init__()
        self.timer = QBasicTimer()
        self._init_ui()
        self.timer.start(1000, self)

    def _init_ui(self):
        self.setWindowTitle('Editor de Texto')
        self.setGeometry(200, 150, 750, 500)

        # =============================
        #  BARRA DE MENÚ (file_dialog.py: QAction, menuBar)
        # =============================
        menubar = self.menuBar()

        # --- Menú Archivo ---
        archivo_menu = menubar.addMenu('&Archivo')

        self.action_seleccionar = QAction('Seleccionar carpeta', self)
        self.action_seleccionar.setShortcut('Ctrl+D')
        self.action_seleccionar.setStatusTip('Seleccionar carpeta de trabajo')
        archivo_menu.addAction(self.action_seleccionar)

        archivo_menu.addSeparator()

        self.action_guardar = QAction('Guardar', self)
        self.action_guardar.setShortcut('Ctrl+S')
        self.action_guardar.setStatusTip('Guardar archivo')
        archivo_menu.addAction(self.action_guardar)

        self.action_guardar_como = QAction('Guardar como...', self)
        self.action_guardar_como.setShortcut('Ctrl+Shift+S')
        self.action_guardar_como.setStatusTip('Guardar archivo con otro nombre')
        archivo_menu.addAction(self.action_guardar_como)

        archivo_menu.addSeparator()

        self.action_salir = QAction('Salir', self)
        self.action_salir.setShortcut('Ctrl+Q')
        archivo_menu.addAction(self.action_salir)

        # --- Menú Edición ---
        edicion_menu = menubar.addMenu('&Edición')

        self.action_buscar = QAction('Buscar y reemplazar', self)
        self.action_buscar.setShortcut('Ctrl+F')
        self.action_buscar.setStatusTip('Buscar texto en el documento')
        edicion_menu.addAction(self.action_buscar)

        # --- Menú Formato ---
        formato_menu = menubar.addMenu('F&ormato')

        self.action_fuente = QAction('Fuente...', self)
        self.action_fuente.setStatusTip('Cambiar fuente del editor')
        formato_menu.addAction(self.action_fuente)

        self.action_color_texto = QAction('Color de texto...', self)
        self.action_color_texto.setStatusTip('Cambiar color del texto')
        formato_menu.addAction(self.action_color_texto)

        self.action_color_fondo = QAction('Color de fondo...', self)
        self.action_color_fondo.setStatusTip('Cambiar color de fondo del editor')
        formato_menu.addAction(self.action_color_fondo)

        # =============================
        #  TOOLBAR (file_dialog.py: toolbar)
        # =============================
        toolbar = self.addToolBar('Herramientas')
        toolbar.addAction(self.action_seleccionar)
        toolbar.addAction(self.action_guardar)
        toolbar.addAction(self.action_fuente)
        toolbar.addAction(self.action_color_texto)

        # =============================
        #  STATUSBAR (file_dialog.py: statusBar)
        # =============================
        self.statusBar().showMessage('Listo')

        # =============================
        #  WIDGET CENTRAL
        # =============================
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        # --- Fila superior: Carpeta (input_dialog.py: QLineEdit, QPushButton) ---
        carpeta_layout = QHBoxLayout()
        lbl_carpeta = QLabel('Carpeta:')
        self.txt_carpeta = QLineEdit()
        self.txt_carpeta.setReadOnly(True)
        self.txt_carpeta.setPlaceholderText('Seleccione una carpeta...')
        self.btn_seleccionar = QPushButton('Seleccionar')
        carpeta_layout.addWidget(lbl_carpeta)
        carpeta_layout.addWidget(self.txt_carpeta)
        carpeta_layout.addWidget(self.btn_seleccionar)
        main_layout.addLayout(carpeta_layout)

        # --- Label "Archivos" (slider.py / calendar.py: QLabel) ---
        lbl_archivos = QLabel('Archivos')
        lbl_archivos.setFont(QFont('Sans', 10, QFont.Bold))
        main_layout.addWidget(lbl_archivos)

        # --- Zona central: Lista + Editor (QSplitter) ---
        splitter = QSplitter(Qt.Horizontal)

        # Lista de archivos (QListWidget)
        self.lista_archivos = QListWidget()
        self.lista_archivos.setSizePolicy(QSizePolicy.Preferred,
                                          QSizePolicy.Expanding)
        splitter.addWidget(self.lista_archivos)

        # Editor de texto (file_dialog.py: QTextEdit)
        self.text_edit = QTextEdit()
        self.text_edit.setFont(QFont('Courier', 13))
        self.text_edit.setPlaceholderText('Seleccione un archivo para editar...')
        splitter.addWidget(self.text_edit)

        splitter.setSizes([150, 450])
        main_layout.addWidget(splitter)

        # --- Separador (toggle_button.py: QFrame) ---
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(sep)

        # --- Fila inferior: opciones y botones ---
        bottom_layout = QHBoxLayout()

        # CheckBox word wrap (check_box.py: QCheckBox + stateChanged)
        self.cb_word_wrap = QCheckBox('Ajuste de línea')
        self.cb_word_wrap.toggle()
        bottom_layout.addWidget(self.cb_word_wrap)

        # Toggle botón solo lectura (toggle_button.py: QPushButton checkable)
        self.btn_solo_lectura = QPushButton('Solo lectura')
        self.btn_solo_lectura.setCheckable(True)
        bottom_layout.addWidget(self.btn_solo_lectura)

        # Slider tamaño fuente (slider.py: QSlider + QLabel)
        slider_lbl = QLabel('Tamaño:')
        self.font_slider = QSlider(Qt.Horizontal)
        self.font_slider.setMinimum(8)
        self.font_slider.setMaximum(36)
        self.font_slider.setValue(13)
        self.font_slider.setFocusPolicy(Qt.NoFocus)
        self.lbl_font_size = QLabel('13')
        bottom_layout.addWidget(slider_lbl)
        bottom_layout.addWidget(self.font_slider)
        bottom_layout.addWidget(self.lbl_font_size)

        bottom_layout.addStretch()

        # ProgressBar para guardar (progressbar.py: QProgressBar + QBasicTimer)
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFixedWidth(120)
        self.progress_bar.hide()
        bottom_layout.addWidget(self.progress_bar)

        # Botones Salvar / Salvar como (QPushButton + signals/slots)
        self.btn_guardar = QPushButton('Salvar')
        self.btn_guardar_como = QPushButton('Salvar como')
        bottom_layout.addWidget(self.btn_guardar)
        bottom_layout.addWidget(self.btn_guardar_como)

        main_layout.addLayout(bottom_layout)

        # --- Label de estado inferior (calendar.py: QLabel) ---
        info_layout = QHBoxLayout()
        self.lbl_info = QLabel('Líneas: 0  |  Caracteres: 0')
        self.lbl_reloj = QLabel('')
        self.lbl_reloj.setAlignment(Qt.AlignRight)
        info_layout.addWidget(self.lbl_info)
        info_layout.addStretch()
        info_layout.addWidget(self.lbl_reloj)
        main_layout.addLayout(info_layout)

    # =============================
    #  TIMER para reloj (progressbar.py: QBasicTimer + timerEvent)
    # =============================

    def timerEvent(self, e):
        from PyQt5.QtCore import QDateTime
        now = QDateTime.currentDateTime()
        self.lbl_reloj.setText(now.toString('hh:mm:ss  —  dd/MM/yyyy'))

    # =============================
    #  MÉTODOS AUXILIARES DE LA VISTA
    # =============================

    def set_carpeta(self, ruta):
        self.txt_carpeta.setText(ruta)

    def set_archivos(self, archivos):
        self.lista_archivos.clear()
        self.lista_archivos.addItems(archivos)

    def set_contenido(self, contenido):
        self.text_edit.setPlainText(contenido)

    def get_contenido(self):
        return self.text_edit.toPlainText()

    def set_titulo(self, titulo):
        self.setWindowTitle(titulo)

    def mostrar_mensaje(self, mensaje):
        self.statusBar().showMessage(mensaje, 4000)

    def mostrar_error(self, mensaje):
        self.statusBar().showMessage(f'⚠ {mensaje}', 5000)

    def actualizar_info(self, lineas, caracteres):
        self.lbl_info.setText(
            f'Líneas: {lineas}  |  Caracteres: {caracteres}')

    def mostrar_progreso(self):
        """Animación de guardado con la progress bar."""
        self.progress_bar.setValue(0)
        self.progress_bar.show()
        self._prog_timer = QBasicTimer()
        self._prog_step = 0
        self._prog_timer.start(15, self._prog_handler_wrapper())

    def _prog_handler_wrapper(self):
        """Devuelve un objeto con timerEvent para animar la barra."""
        bar = self.progress_bar

        class _Anim:
            def __init__(self):
                self.step = 0
                self.timer = QBasicTimer()

            def start(self):
                self.step = 0
                bar.setValue(0)
                bar.show()
                self.timer.start(15, bar)

        return bar

    def animar_progreso(self, valor):
        self.progress_bar.setValue(valor)
        if valor >= 100:
            from PyQt5.QtCore import QTimer
            QTimer.singleShot(600, self.progress_bar.hide)
