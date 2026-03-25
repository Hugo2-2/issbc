"""
Modelo del editor de texto (MVC - Model).
Gestiona el estado de los archivos: carpeta actual, lista de archivos,
contenido del archivo abierto, y operaciones de lectura/escritura.
"""

import os
from PyQt5.QtCore import QObject, pyqtSignal


class EditorModel(QObject):
    """Modelo que gestiona los datos y la lógica de negocio del editor."""

    # Señales personalizadas (custom_signal.py / signal_slots.py)
    carpeta_cambiada = pyqtSignal(str)
    archivos_actualizados = pyqtSignal(list)
    archivo_abierto = pyqtSignal(str, str)       # (nombre, contenido)
    archivo_guardado = pyqtSignal(str)
    error_ocurrido = pyqtSignal(str)
    estado_modificado = pyqtSignal(bool)          # archivo modificado

    def __init__(self):
        super().__init__()
        self._carpeta_actual = ''
        self._archivo_actual = ''
        self._contenido_original = ''
        self._modificado = False
        self._extensiones = ('.txt', '.py', '.html', '.css', '.js',
                             '.json', '.xml', '.md', '.csv', '.log',
                             '.cfg', '.ini', '.yml', '.yaml')

    # --- Propiedades ---

    @property
    def carpeta_actual(self):
        return self._carpeta_actual

    @property
    def archivo_actual(self):
        return self._archivo_actual

    @property
    def modificado(self):
        return self._modificado

    # --- Operaciones de carpeta ---

    def seleccionar_carpeta(self, ruta):
        """Establece la carpeta y emite la lista de archivos."""
        if os.path.isdir(ruta):
            self._carpeta_actual = ruta
            self.carpeta_cambiada.emit(ruta)
            self._listar_archivos()
        else:
            self.error_ocurrido.emit(f'La carpeta no existe: {ruta}')

    def _listar_archivos(self):
        """Lista archivos de texto en la carpeta actual."""
        try:
            archivos = []
            for f in sorted(os.listdir(self._carpeta_actual)):
                ruta_completa = os.path.join(self._carpeta_actual, f)
                if os.path.isfile(ruta_completa):
                    _, ext = os.path.splitext(f)
                    if ext.lower() in self._extensiones:
                        archivos.append(f)
            self.archivos_actualizados.emit(archivos)
        except OSError as e:
            self.error_ocurrido.emit(f'Error al listar archivos: {e}')

    # --- Operaciones de archivo ---

    def abrir_archivo(self, nombre):
        """Abre un archivo de la carpeta actual."""
        ruta = os.path.join(self._carpeta_actual, nombre)
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                contenido = f.read()
            self._archivo_actual = ruta
            self._contenido_original = contenido
            self._modificado = False
            self.estado_modificado.emit(False)
            self.archivo_abierto.emit(nombre, contenido)
        except Exception as e:
            self.error_ocurrido.emit(f'Error al abrir: {e}')

    def guardar(self, contenido):
        """Guarda el contenido en el archivo actual."""
        if not self._archivo_actual:
            self.error_ocurrido.emit('No hay archivo abierto para guardar.')
            return False
        return self._escribir(self._archivo_actual, contenido)

    def guardar_como(self, ruta, contenido):
        """Guarda el contenido en una ruta específica."""
        return self._escribir(ruta, contenido)

    def _escribir(self, ruta, contenido):
        """Escribe contenido en disco."""
        try:
            with open(ruta, 'w', encoding='utf-8') as f:
                f.write(contenido)
            self._archivo_actual = ruta
            self._contenido_original = contenido
            self._modificado = False
            self.estado_modificado.emit(False)
            nombre = os.path.basename(ruta)
            self.archivo_guardado.emit(nombre)
            # Refrescar lista por si se creó un archivo nuevo
            if os.path.dirname(ruta) == self._carpeta_actual:
                self._listar_archivos()
            return True
        except Exception as e:
            self.error_ocurrido.emit(f'Error al guardar: {e}')
            return False

    def marcar_modificado(self, contenido_actual):
        """Compara el contenido actual con el original."""
        mod = contenido_actual != self._contenido_original
        if mod != self._modificado:
            self._modificado = mod
            self.estado_modificado.emit(mod)
