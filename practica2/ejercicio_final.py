#!/usr/bin/python

"""
Calculadora con Notas – Práctica II (ISSBC)
============================================
Calculadora funcional con panel de notas que integra todos los
elementos de 'events_and_signals' y 'layout_managment'.

  · signal_slots.py        → QSlider conectado al brillo del LCD
  · custom_signal.py       → pyqtSignal emitida al obtener un resultado
  · event_object.py        → mouseMoveEvent muestra coordenadas en statusbar
  · event_sender.py        → sender() identifica qué botón se pulsó
  · reimplement_handler.py → keyPressEvent para entrada por teclado / Escape
  · absolute.py            → Labels posicionadas con move()
  · box_layout.py          → QHBoxLayout + QVBoxLayout para la estructura
  · calculator.py          → QGridLayout con los botones de la calculadora
  · review.py              → QGridLayout con formulario (QLabel+QLineEdit+QTextEdit)
"""

import sys
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QLCDNumber, QSlider,
    QLineEdit, QTextEdit, QMessageBox
)
from PyQt5.QtGui import QFont


# ── Señal personalizada (custom_signal.py) ────────────────────────────
class Communicate(QObject):
    """Emite una señal con el texto del resultado de cada operación."""
    newResult = pyqtSignal(str)


# ── Ventana principal ─────────────────────────────────────────────────
class Calculadora(QMainWindow):

    def __init__(self):
        super().__init__()
        self.c = Communicate()
        self.c.newResult.connect(self._add_to_history)   # signal_slots.py
        self.expr = ''
        self._init_ui()

    # ----------------------------------------------------------------
    # UI
    # ----------------------------------------------------------------
    def _init_ui(self):
        self.setWindowTitle('Calculadora + Notas – Práctica II')
        self.setGeometry(250, 150, 720, 480)

        # Barra de estado — mostrará coords del ratón (event_object.py)
        self.sbar = self.statusBar()
        self.sbar.showMessage('Listo · Escribe con el teclado o pulsa los botones')

        central = QWidget()
        root = QHBoxLayout()                              # box_layout.py

        # ── Columna izquierda: calculadora ────────────────────────────
        calc_col = QVBoxLayout()                          # box_layout.py

        # Título con posicionamiento absoluto (absolute.py)
        header = QWidget()
        header.setFixedHeight(28)
        lbl_icon = QLabel('🧮', header)
        lbl_icon.move(0, 2)
        lbl_title = QLabel('Calculadora', header)
        lbl_title.setFont(QFont('Sans Serif', 12, QFont.Bold))
        lbl_title.move(24, 2)
        calc_col.addWidget(header)

        # Pantalla LCD (signal_slots.py: el slider controla su brillo)
        self.lcd = QLCDNumber()
        self.lcd.setDigitCount(12)
        self.lcd.setMinimumHeight(52)
        self.lcd.setSegmentStyle(QLCDNumber.Flat)
        calc_col.addWidget(self.lcd)

        # Campo de expresión
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFont(QFont('Courier', 15))
        self.display.setPlaceholderText('0')
        calc_col.addWidget(self.display)

        # Rejilla de botones (calculator.py → QGridLayout)
        grid = QGridLayout()
        names = ['C', '⌫', '%', '/',
                 '7', '8', '9', '×',
                 '4', '5', '6', '-',
                 '1', '2', '3', '+',
                 '±', '0', '.', '=']
        positions = [(i, j) for i in range(5) for j in range(4)]
        for pos, name in zip(positions, names):
            btn = QPushButton(name)
            btn.setMinimumSize(52, 38)
            btn.clicked.connect(self._btn_clicked)        # event_sender.py
            grid.addWidget(btn, *pos)
        calc_col.addLayout(grid)

        # Slider de brillo LCD (signal_slots.py: valueChanged → slot)
        bright_row = QHBoxLayout()
        bright_row.addWidget(QLabel('Brillo LCD:'))
        self.bright_slider = QSlider(Qt.Horizontal)
        self.bright_slider.setRange(10, 100)
        self.bright_slider.setValue(100)
        self.bright_slider.valueChanged.connect(self._set_lcd_opacity)
        bright_row.addWidget(self.bright_slider)
        calc_col.addLayout(bright_row)

        root.addLayout(calc_col, 3)

        # ── Columna derecha: notas (review.py → QGridLayout + form) ──
        notes_col = QVBoxLayout()

        note_header = QWidget()
        note_header.setFixedHeight(28)
        QLabel('📋 Notas', note_header).move(0, 2)       # absolute.py
        notes_col.addWidget(note_header)

        form = QGridLayout()                              # review.py
        form.setSpacing(8)

        form.addWidget(QLabel('Título:'), 0, 0)
        self.note_title = QLineEdit()
        self.note_title.setPlaceholderText('Nombre del cálculo…')
        form.addWidget(self.note_title, 0, 1)

        form.addWidget(QLabel('Historial:'), 1, 0, Qt.AlignTop)
        self.history = QTextEdit()
        self.history.setReadOnly(True)
        self.history.setPlaceholderText('Los resultados aparecerán aquí…')
        form.addWidget(self.history, 1, 1, 3, 1)

        form.addWidget(QLabel('Notas:'), 4, 0, Qt.AlignTop)
        self.notes = QTextEdit()
        self.notes.setPlaceholderText('Escribe tus notas…')
        form.addWidget(self.notes, 4, 1, 3, 1)

        notes_col.addLayout(form)

        # Botones limpiar (box_layout.py: HBox alineado a la derecha)
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        btn_ch = QPushButton('Limpiar historial')
        btn_cn = QPushButton('Limpiar notas')
        btn_ch.clicked.connect(lambda: self.history.clear())
        btn_cn.clicked.connect(lambda: self.notes.clear())
        hbox.addWidget(btn_ch)
        hbox.addWidget(btn_cn)
        notes_col.addLayout(hbox)

        root.addLayout(notes_col, 2)

        central.setLayout(root)
        self.setCentralWidget(central)
        self.show()

    # ----------------------------------------------------------------
    # Slots
    # ----------------------------------------------------------------
    def _btn_clicked(self):
        """Identifica el botón con sender() (event_sender.py)."""
        text = self.sender().text()
        self.sbar.showMessage(f'Botón: {text}')

        if text == '=':
            self._calculate()
        elif text == 'C':
            self.expr = ''
            self.display.clear()
            self.lcd.display(0)
        elif text == '⌫':
            self.expr = self.expr[:-1]
            self.display.setText(self.expr)
        elif text == '±':
            if self.expr.startswith('-'):
                self.expr = self.expr[1:]
            elif self.expr:
                self.expr = '-' + self.expr
            self.display.setText(self.expr)
        else:
            self.expr += '*' if text == '×' else text
            self.display.setText(self.expr)

    def _calculate(self):
        """Evalúa y emite la señal personalizada (custom_signal.py)."""
        try:
            safe = self.expr.replace('%', '/100')
            result = round(eval(safe), 10)
            self.lcd.display(result)
            self.display.setText(str(result))
            self.c.newResult.emit(f'{self.expr} = {result}')
            self.expr = str(result)
        except Exception:
            self.display.setText('Error')
            self.expr = ''

    def _add_to_history(self, text):
        """Slot conectado a la señal newResult (signal_slots.py)."""
        self.history.append(text)

    def _set_lcd_opacity(self, value):
        """Slot del slider: ajusta el estilo del LCD (signal_slots.py)."""
        alpha = value / 100
        self.lcd.setStyleSheet(f'opacity: {alpha}; color: rgba(0,0,0,{alpha});')
        self.sbar.showMessage(f'Brillo LCD: {value}%')

    # ----------------------------------------------------------------
    # Eventos reimplementados
    # ----------------------------------------------------------------
    def mouseMoveEvent(self, e):
        """Muestra coordenadas del ratón en la statusbar (event_object.py)."""
        self.sbar.showMessage(f'x: {e.x()},  y: {e.y()}')

    def keyPressEvent(self, e):
        """Entrada por teclado y Escape para salir (reimplement_handler.py)."""
        key = e.key()
        if key == Qt.Key_Escape:
            self.close()
        elif key in (Qt.Key_Return, Qt.Key_Enter):
            self._calculate()
        elif key == Qt.Key_Backspace:
            self.expr = self.expr[:-1]
            self.display.setText(self.expr)
        elif e.text() in '0123456789.+-*/()%':
            self.expr += e.text()
            self.display.setText(self.expr)

    def closeEvent(self, event):
        """Confirmación al cerrar (QMessageBox)."""
        reply = QMessageBox.question(
            self, 'Salir', '¿Cerrar la calculadora?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        event.accept() if reply == QMessageBox.Yes else event.ignore()


# ── Punto de entrada ──────────────────────────────────────────────────
def main():
    app = QApplication(sys.argv)
    app.setFont(QFont('Sans Serif', 10))
    ex = Calculadora()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
