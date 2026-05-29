import os
import sys

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QButtonGroup, QComboBox,
    QLineEdit, QFileDialog, QFrame, QMessageBox, QSizePolicy,
    QGraphicsDropShadowEffect, QStackedWidget, QScrollArea,
)
from PyQt6.QtCore import (
    Qt, pyqtSignal,
)
from PyQt6.QtGui import  QColor

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controllers import AESController
from models import AESMode

"""Variables Globales"""
BG_BASE = "#0b0e17"
BG_SURFACE = "#111520"
BG_ELEVATED = "#171c2e"
BG_INPUT = "#0e1119"
BG_HOVER = "#1a2035"

ACCENT = "#6c8fff"
ACCENT_DIM = "#3a5acc"
ACCENT_GLOW = "rgba(108,143,255,0.12)"
ACCENT_GLOW2 = "rgba(108,143,255,0.06)"

SUCCESS = "#3ecf8e"
DANGER = "#f0607a"

TEXT_PRI = "#e8eaf0"
TEXT_SEC = "#6e7a99"
TEXT_HINT = "#3a4260"

BORDER = "#1e2440"
BORDER_EM = "#2a3360"
BORDER_ACC = "#3a5acc"

RADIUS_SM = "6px"
RADIUS_MD = "10px"
RADIUS_LG = "14px"

MONO = '"JetBrains Mono", "Fira Code", "Consolas", monospace'
SANS = '"Segoe UI", "Inter", "SF Pro Display", sans-serif'


"""Hoja de estilo"""
STYLESHEET = f"""
/*Base*/
QMainWindow, QWidget#centralWidget, QWidget#scrollContent {{
    background-color: {BG_BASE};
}}
QWidget {{
    color: {TEXT_PRI};
    font-family: {SANS};
    font-size: 13px;
}}

/*ScrollArea*/
QScrollArea {{
    background: transparent;
    border: none;
}}
QScrollBar:vertical {{
    background: transparent;
    width: 5px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: {BORDER_EM};
    border-radius: 3px;
    min-height: 32px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{ background: none; }}

/*Labels*/
QLabel#mainTitle {{
    color: {TEXT_PRI};
    font-family: {SANS};
    font-size: 22px;
    font-weight: 600;
    letter-spacing: -0.3px;
}}
QLabel#tagLine {{
    color: {TEXT_SEC};
    font-family: {MONO};
    font-size: 10px;
    letter-spacing: 2px;
}}
QLabel#nistBadge {{
    color: {ACCENT};
    font-family: {MONO};
    font-size: 9px;
    letter-spacing: 1px;
    padding: 3px 8px;
    border: 1px solid {BORDER_ACC};
    border-radius: {RADIUS_SM};
    background: {ACCENT_GLOW2};
}}
QLabel#stepLabel {{
    color: {ACCENT};
    font-family: {MONO};
    font-size: 9px;
    letter-spacing: 3px;
    font-weight: 600;
}}
QLabel#cardTitle {{
    color: {TEXT_PRI};
    font-size: 14px;
    font-weight: 600;
}}
QLabel#fieldLabel {{
    color: {TEXT_SEC};
    font-family: {MONO};
    font-size: 9px;
    letter-spacing: 2px;
}}
QLabel#hintLabel {{
    color: {TEXT_HINT};
    font-family: {MONO};
    font-size: 9px;
    letter-spacing: 1px;
}}
QLabel#modeBadge {{
    color: {SUCCESS};
    font-family: {MONO};
    font-size: 9px;
    padding: 2px 8px;
    border: 1px solid rgba(62,207,142,0.25);
    border-radius: 4px;
    background: rgba(62,207,142,0.06);
}}
QLabel#statusOk {{
    color: {SUCCESS};
    font-family: {MONO};
    font-size: 10px;
}}
QLabel#statusErr {{
    color: {DANGER};
    font-family: {MONO};
    font-size: 10px;
}}

/*Cards*/
QFrame#card {{
    background: {BG_SURFACE};
    border: 1px solid {BORDER};
    border-radius: {RADIUS_LG};
}}
QFrame#cardAccent {{
    background: {BG_SURFACE};
    border: 1px solid {BORDER_ACC};
    border-radius: {RADIUS_LG};
}}
QFrame#divider {{
    background: {BORDER};
    min-height: 1px;
    max-height: 1px;
}}
QFrame#pill {{
    background: {BG_ELEVATED};
    border: 1px solid {BORDER};
    border-radius: 99px;
}}

/*Inputs*/
QLineEdit {{
    background: {BG_INPUT};
    color: {TEXT_PRI};
    border: 1px solid {BORDER};
    border-radius: {RADIUS_SM};
    padding: 9px 12px;
    font-family: {MONO};
    font-size: 12px;
    selection-background-color: {ACCENT};
    selection-color: #fff;
}}
QLineEdit:focus {{
    border: 1px solid {ACCENT};
    background: #0f1220;
}}
QLineEdit:disabled {{
    color: {TEXT_HINT};
    border-color: {BORDER};
    background: {BG_BASE};
}}
QLineEdit[readOnly="true"] {{
    color: {TEXT_SEC};
}}

/*ComboBox*/
QComboBox {{
    background: {BG_INPUT};
    color: {TEXT_PRI};
    border: 1px solid {BORDER};
    border-radius: {RADIUS_SM};
    padding: 9px 36px 9px 12px;
    font-family: {MONO};
    font-size: 12px;
    min-width: 140px;
}}
QComboBox:focus, QComboBox:on {{
    border: 1px solid {ACCENT};
}}
QComboBox::drop-down {{
    border: none;
    width: 32px;
}}
QComboBox::down-arrow {{
    width: 0; height: 0;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid {ACCENT};
    margin-right: 10px;
}}
QComboBox QAbstractItemView {{
    background: {BG_ELEVATED};
    color: {TEXT_PRI};
    border: 1px solid {BORDER_ACC};
    border-radius: {RADIUS_MD};
    selection-background-color: {ACCENT_GLOW};
    selection-color: {TEXT_PRI};
    font-family: {MONO};
    font-size: 12px;
    outline: none;
    padding: 4px;
}}

/*Radio buttons*/
QRadioButton {{
    color: {TEXT_SEC};
    font-family: {SANS};
    font-size: 13px;
    font-weight: 500;
    spacing: 8px;
    padding: 0 4px;
}}
QRadioButton:checked {{
    color: {TEXT_PRI};
}}
QRadioButton::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 9px;
    border: 2px solid {BORDER_EM};
    background: {BG_INPUT};
}}
QRadioButton::indicator:checked {{
    border: 2px solid {ACCENT};
    background: qradialgradient(cx:0.5, cy:0.5, radius:0.5,
        fx:0.5, fy:0.5,
        stop:0 {ACCENT}, stop:0.45 {ACCENT},
        stop:0.46 {BG_INPUT}, stop:1 {BG_INPUT});
}}
QRadioButton::indicator:hover {{
    border-color: {ACCENT_DIM};
}}

/*Buttons*/
QPushButton#primaryBtn {{
    background: {ACCENT};
    color: #fff;
    border: none;
    border-radius: {RADIUS_SM};
    padding: 10px 20px;
    font-family: {SANS};
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.3px;
}}
QPushButton#primaryBtn:hover {{
    background: #7fa0ff;
}}
QPushButton#primaryBtn:pressed {{
    background: {ACCENT_DIM};
}}

QPushButton#ghostBtn {{
    background: transparent;
    color: {ACCENT};
    border: 1px solid {BORDER_ACC};
    border-radius: {RADIUS_SM};
    padding: 8px 14px;
    font-family: {MONO};
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 1px;
}}
QPushButton#ghostBtn:hover {{
    background: {ACCENT_GLOW};
}}
QPushButton#ghostBtn:pressed {{
    background: rgba(108,143,255,0.18);
}}

QPushButton#execBtn {{
    background: {ACCENT};
    color: #fff;
    border: none;
    border-radius: {RADIUS_MD};
    padding: 13px 32px;
    font-family: {SANS};
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.2px;
    min-width: 200px;
}}
QPushButton#execBtn:hover {{
    background: #7fa0ff;
}}
QPushButton#execBtn:pressed {{
    background: {ACCENT_DIM};
}}
"""

"""Helpers"""
def h_divider() -> QFrame:
    d = QFrame()
    d.setObjectName("divider")
    d.setFrameShape(QFrame.Shape.HLine)
    return d


def card(accent: bool = False) -> QFrame:
    f = QFrame()
    f.setObjectName("cardAccent" if accent else "card")
    return f


def drop_shadow(w: QWidget, blur: int = 20) -> None:
    eff = QGraphicsDropShadowEffect()
    eff.setBlurRadius(blur)
    eff.setColor(QColor(0, 0, 0, 80))
    eff.setOffset(0, 6)
    w.setGraphicsEffect(eff)


class FilePickerField(QWidget):
    file_selected = pyqtSignal(str)

    def __init__(self, label: str, filter_str: str = "All Files (*)", parent=None):
        super().__init__(parent)
        self._filter = filter_str
        self._path = ""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        lbl = QLabel(label)
        lbl.setObjectName("fieldLabel")
        layout.addWidget(lbl)

        row = QHBoxLayout()
        row.setSpacing(8)
        self._edit = QLineEdit()
        self._edit.setPlaceholderText("Sin archivo seleccionado…")
        self._edit.setReadOnly(True)
        row.addWidget(self._edit, 1)

        btn = QPushButton("EXAMINAR")
        btn.setObjectName("ghostBtn")
        btn.setFixedWidth(100)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(self._browse)
        row.addWidget(btn)
        layout.addLayout(row)

    def _browse(self):
        path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo", "", self._filter)
        if path:
            self._path = path
            self._edit.setText(path)
            self.file_selected.emit(path)

    def get_path(self) -> str:
        return self._path

    def clear(self):
        self._path = ""
        self._edit.clear()


class StepHeader(QWidget):
    def __init__(self, step: str, title: str, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        # Number badge
        badge = QLabel(step)
        badge.setFixedSize(28, 28)
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setStyleSheet(f"""
            background: {ACCENT_GLOW};
            color: {ACCENT};
            border: 1px solid {BORDER_ACC};
            border-radius: 14px;
            font-family: {MONO};
            font-size: 10px;
            font-weight: 700;
        """)
        layout.addWidget(badge)

        title_lbl = QLabel(title)
        title_lbl.setObjectName("cardTitle")
        layout.addWidget(title_lbl)
        layout.addStretch()


class OperationToggle(QFrame):
    
    changed = pyqtSignal(int)   # 1=cifrar, 2=descifrar

    _OPTS = [("Cifrar", 1), ("Descifrar", 2)]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("pill")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(2)

        # exclusive=False hace que ninguno esté seleccionado al inicio
        self._group = QButtonGroup(self)
        self._group.setExclusive(False)
        self._buttons: list[QPushButton] = []

        for label, idx in self._OPTS:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setFixedHeight(34)
            self._style_btn(btn, False)
            self._group.addButton(btn, idx)
            self._buttons.append(btn)
            layout.addWidget(btn)

        self._group.idClicked.connect(self._on_clicked)

    def _style_btn(self, btn: QPushButton, active: bool):
        if active:
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: {ACCENT};
                    color: #fff;
                    border: none;
                    border-radius: 7px;
                    font-size: 13px;
                    font-weight: 600;
                    padding: 0 22px;
                    font-family: {SANS};
                }}
            """)
        else:
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    color: {TEXT_SEC};
                    border: none;
                    border-radius: 7px;
                    font-size: 13px;
                    font-weight: 500;
                    padding: 0 22px;
                    font-family: {SANS};
                }}
                QPushButton:hover {{
                    background: {ACCENT_GLOW2};
                    color: {TEXT_PRI};
                }}
            """)

    def _on_clicked(self, idx: int):
        # Desmarca el otro botón
        for btn in self._buttons:
            active = self._group.id(btn) == idx
            btn.setChecked(active)
            self._style_btn(btn, active)
        self.changed.emit(idx)

"""Panel para Cifrar"""
class EncryptPanel(QWidget):
    def __init__(self, controller: AESController, parent=None):
        super().__init__(parent)
        self._ctrl = controller
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        self._file_picker = FilePickerField("ARCHIVO A CIFRAR")
        layout.addWidget(self._file_picker)

        self._key_picker = FilePickerField(
            "ARCHIVO DE LLAVE", "Key Files (*.key);;All Files (*)"
        )
        layout.addWidget(self._key_picker)

        # Mode + IV
        self._mode_iv = QWidget()
        self._mode_iv_layout = QHBoxLayout(self._mode_iv)
        self._mode_iv_layout.setContentsMargins(0, 0, 0, 0)
        self._mode_iv_layout.setSpacing(16)

        # Mode column
        mode_col = QVBoxLayout()
        mode_col.setSpacing(5)
        mode_lbl = QLabel("MODO DE OPERACIÓN")
        mode_lbl.setObjectName("fieldLabel")
        mode_col.addWidget(mode_lbl)
        self._mode_combo = QComboBox()
        for m in self._ctrl.get_modes():
            self._mode_combo.addItem(m)
        self._mode_combo.currentTextChanged.connect(self._on_mode_changed)
        mode_col.addWidget(self._mode_combo)
        self._mode_badge = QLabel()
        self._mode_badge.setObjectName("modeBadge")
        mode_col.addWidget(self._mode_badge)
        self._mode_iv_layout.addLayout(mode_col)

        # IV column
        iv_col = QVBoxLayout()
        iv_col.setSpacing(5)
        self._iv_lbl = QLabel("VECTOR DE INICIALIZACIÓN")
        self._iv_lbl.setObjectName("fieldLabel")
        iv_col.addWidget(self._iv_lbl)
        self._iv_edit = QLineEdit()
        self._iv_edit.setPlaceholderText("Ingrese IV alfanumérico…")
        iv_col.addWidget(self._iv_edit)
        self._iv_hint = QLabel()
        self._iv_hint.setObjectName("hintLabel")
        iv_col.addWidget(self._iv_hint)
        self._mode_iv_layout.addLayout(iv_col, 1)

        layout.addWidget(self._mode_iv)

        # Execute
        btn_row = QHBoxLayout()
        self._exec_btn = QPushButton("Cifrar archivo")
        self._exec_btn.setObjectName("execBtn")
        self._exec_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._exec_btn.clicked.connect(self._execute)
        btn_row.addStretch()
        btn_row.addWidget(self._exec_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        self._status = QLabel("")
        self._status.setObjectName("statusOk")
        self._status.setWordWrap(True)
        self._status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._status)

        self._on_mode_changed(self._mode_combo.currentText())

    def _on_mode_changed(self, mode_name: str):
        self._mode_badge.setText(self._ctrl.get_mode_description(mode_name))
        iv_size = self._ctrl.get_iv_size_for_mode(mode_name)
        needs = self._ctrl.mode_requires_iv(mode_name)
        self._iv_edit.setEnabled(needs)
        if needs:
            self._iv_edit.setMaxLength(iv_size)
            self._iv_edit.setPlaceholderText(f"Exactamente {iv_size} caracteres ASCII")
            self._iv_hint.setText(f"↳ {iv_size} bytes requeridos para {mode_name}")
        else:
            self._iv_edit.clear()
            self._iv_edit.setPlaceholderText("No requerido para ECB")
            self._iv_hint.setText("↳ ECB no utiliza IV (NIST SP 800-38A)")

    def _execute(self):
        self._status.setText("")
        mode = AESMode(self._mode_combo.currentText())
        out_dir = QFileDialog.getExistingDirectory(self, "Seleccionar directorio de salida")
        if not out_dir:
            return
        ok, msg = self._ctrl.encrypt(
            self._file_picker.get_path(),
            self._key_picker.get_path(),
            mode,
            self._iv_edit.text(),
            out_dir,
        )
        self._set_status(ok, msg)

    def _set_status(self, ok: bool, msg: str):
        self._status.setObjectName("statusOk" if ok else "statusErr")
        self._status.setText(("✓  " if ok else "✗  ") + msg)
        self._status.style().unpolish(self._status)
        self._status.style().polish(self._status)
        if ok:
            QMessageBox.information(self, "Operación exitosa", msg)
        else:
            QMessageBox.critical(self, "Error", msg)

"""Panel para Descifrar"""
class DecryptPanel(QWidget):
    def __init__(self, controller: AESController, parent=None):
        super().__init__(parent)
        self._ctrl = controller
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        self._file_picker = FilePickerField("ARCHIVO A DESCIFRAR")
        layout.addWidget(self._file_picker)

        self._key_picker = FilePickerField(
            "ARCHIVO DE LLAVE", "Key Files (*.key);;All Files (*)"
        )
        layout.addWidget(self._key_picker)

        mode_col = QVBoxLayout()
        mode_col.setSpacing(5)
        mode_lbl = QLabel("MODO DE OPERACIÓN")
        mode_lbl.setObjectName("fieldLabel")
        mode_col.addWidget(mode_lbl)
        self._mode_combo = QComboBox()
        for m in self._ctrl.get_modes():
            self._mode_combo.addItem(m)
        self._mode_combo.currentTextChanged.connect(self._on_mode_changed)
        mode_col.addWidget(self._mode_combo)
        self._mode_badge = QLabel()
        self._mode_badge.setObjectName("modeBadge")
        mode_col.addWidget(self._mode_badge)
        layout.addLayout(mode_col)

        btn_row = QHBoxLayout()
        self._exec_btn = QPushButton("Descifrar archivo")
        self._exec_btn.setObjectName("execBtn")
        self._exec_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._exec_btn.clicked.connect(self._execute)
        btn_row.addStretch()
        btn_row.addWidget(self._exec_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        self._status = QLabel("")
        self._status.setObjectName("statusOk")
        self._status.setWordWrap(True)
        self._status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._status)

        self._on_mode_changed(self._mode_combo.currentText())

    def _on_mode_changed(self, mode_name: str):
        self._mode_badge.setText(self._ctrl.get_mode_description(mode_name))

    def _execute(self):
        self._status.setText("")
        mode = AESMode(self._mode_combo.currentText())
        out_dir = QFileDialog.getExistingDirectory(self, "Seleccionar directorio de salida")
        if not out_dir:
            return
        ok, msg = self._ctrl.decrypt(
            self._file_picker.get_path(),
            self._key_picker.get_path(),
            mode,
            out_dir,
        )
        self._set_status(ok, msg)

    def _set_status(self, ok: bool, msg: str):
        self._status.setObjectName("statusOk" if ok else "statusErr")
        self._status.setText(("✓  " if ok else "✗  ") + msg)
        self._status.style().unpolish(self._status)
        self._status.style().polish(self._status)
        if ok:
            QMessageBox.information(self, "Operación exitosa", msg)
        else:
            QMessageBox.critical(self, "Error", msg)


"""Ventana principal"""
class MainView(QMainWindow):

    _MIN_W = 520
    _COMPACT_W = 680   # Ancho máximo para activar el layout expandido

    def __init__(self, controller: AESController):
        super().__init__()
        self._ctrl = controller
        self._setup_window()
        self._setup_ui()

    # Ventana
    def _setup_window(self):
        self.setWindowTitle("Práctica · Cifrador por Bloques (AES)")
        self.setMinimumWidth(self._MIN_W)
        self.setMinimumHeight(480)
        self.resize(780, 720)
        screen = QApplication.primaryScreen().availableGeometry()
        self.move(
            (screen.width()  - self.width())  // 2,
            (screen.height() - self.height()) // 2,
        )

    # GUI
    def _setup_ui(self):
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.setCentralWidget(scroll)

        content = QWidget()
        content.setObjectName("scrollContent")
        scroll.setWidget(content)

        self._root = QVBoxLayout(content)
        self._root.setContentsMargins(28, 24, 28, 32)
        self._root.setSpacing(16)

        self._build_header()
        self._root.addWidget(h_divider())
        self._build_key_card()
        self._build_operation_card()
        self._build_op_panel_card()
        self._root.addStretch()

    # Header
    def _build_header(self):
        hdr = QVBoxLayout()
        hdr.setSpacing(6)

        tag = QLabel("INTRODUCTION TO CRYPTOGRAPHY")
        tag.setObjectName("tagLine")
        hdr.addWidget(tag)

        title = QLabel("Práctica. Cifrador por Bloques (AES)")
        title.setObjectName("mainTitle")
        hdr.addWidget(title)

        badges_row = QHBoxLayout()
        badges_row.setSpacing(6)
        for text in ("FIPS 197", "NIST SP 800-38A", "NIST SP 800-38D", "AES-256"):
            b = QLabel(text)
            b.setObjectName("nistBadge")
            badges_row.addWidget(b)
        badges_row.addStretch()
        hdr.addLayout(badges_row)

        self._root.addLayout(hdr)

    # Tarjeta de Generación de Llaves
    def _build_key_card(self):
        c = card()
        drop_shadow(c)
        lay = QVBoxLayout(c)
        lay.setContentsMargins(20, 18, 20, 18)
        lay.setSpacing(12)

        lay.addWidget(StepHeader("01", "Generación de Llave"))

        desc = QLabel(
            "Genera una Llave AES-256 (32 bytes / 256 bits).\n"
            "Formato: AES_KEY_[DD-MM-YYYY_HH-MM].key"
        )
        desc.setWordWrap(True)
        desc.setStyleSheet(f"color: {TEXT_SEC}; font-size: 12px;")
        lay.addWidget(desc)

        btn_row = QHBoxLayout()
        self._key_btn = QPushButton("Generar y guardar Llave AES-256")
        self._key_btn.setObjectName("primaryBtn")
        self._key_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._key_btn.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        self._key_btn.clicked.connect(self._generate_key)
        btn_row.addWidget(self._key_btn)
        btn_row.addStretch()
        lay.addLayout(btn_row)

        self._root.addWidget(c)

    # Selector de operación
    def _build_operation_card(self):
        c = card()
        drop_shadow(c)
        lay = QVBoxLayout(c)
        lay.setContentsMargins(20, 18, 20, 18)
        lay.setSpacing(14)

        lay.addWidget(StepHeader("02", "Operación"))

        desc = QLabel("Selecciona si deseas cifrar o descifrar un archivo.")
        desc.setStyleSheet(f"color: {TEXT_SEC}; font-size: 12px;")
        lay.addWidget(desc)

        self._toggle = OperationToggle()
        self._toggle.changed.connect(self._on_op_changed)
        # Constrain toggle width so it doesn't stretch uglily
        self._toggle.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        lay.addWidget(self._toggle)

        self._root.addWidget(c)

    # Tarjeta de operación dinámica
    def _build_op_panel_card(self):
        self._op_card = card(accent=True)
        drop_shadow(self._op_card, 28)
        lay = QVBoxLayout(self._op_card)
        lay.setContentsMargins(20, 18, 20, 20)
        lay.setSpacing(14)

        self._op_step = StepHeader("03", "")
        lay.addWidget(self._op_step)

        lay.addWidget(h_divider())

        self._stack = QStackedWidget()
        self._page_empty = QWidget()
        self._page_enc   = EncryptPanel(self._ctrl)
        self._page_dec   = DecryptPanel(self._ctrl)
        self._stack.addWidget(self._page_empty)   # 0
        self._stack.addWidget(self._page_enc)     # 1
        self._stack.addWidget(self._page_dec)     # 2

        lay.addWidget(self._stack)
        self._op_card.setVisible(False)
        self._root.addWidget(self._op_card)

    # Slots
    def _generate_key(self):
        directory = QFileDialog.getExistingDirectory(
            self, "Seleccionar directorio para guardar la Llave"
        )
        if not directory:
            return
        ok, msg = self._ctrl.generate_and_save_key(directory)
        if ok:
            QMessageBox.information(self, "Llave generada", msg)
        else:
            QMessageBox.critical(self, "Error", msg)

    def _on_op_changed(self, idx: int):
        titles = {1: "Cifrado AES", 2: "Descifrado AES"}
        title_lbl = self._op_step.findChild(QLabel, "cardTitle")
        if title_lbl:
            title_lbl.setText(titles[idx])
        self._stack.setCurrentIndex(idx)
        self._op_card.setVisible(True)

    # Responsividad
    def resizeEvent(self, event):
        super().resizeEvent(event)

        # Ajusta el margen en función del ancho
        w = self.width()
        h_margin = max(16, min(48, int(w * 0.045)))
        self._root.setContentsMargins(h_margin, 24, h_margin, 32)