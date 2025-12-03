"""
Inspector Panel - Clip In/Out Editor

Provides UI to view and edit the selected clip's name and In/Out points.
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QGroupBox
)
from PyQt5.QtCore import pyqtSignal


def ms_to_mmssms(ms: int) -> str:
    if ms is None or ms < 0:
        return "00:00.000"
    s, milli = divmod(ms, 1000)
    m, sec = divmod(s, 60)
    return f"{m:02d}:{sec:02d}.{milli:03d}"


def mmssms_to_ms(text: str) -> int:
    """Parse mm:ss.mmm to milliseconds. Returns -1 if invalid."""
    try:
        if not text:
            return -1
        if "." in text:
            minsec, mmm = text.split(".")
            mmm = int(mmm.ljust(3, '0')[:3])
        else:
            minsec, mmm = text, 0
        mm, ss = minsec.split(":")
        mm = int(mm)
        ss = int(ss)
        if mm < 0 or ss < 0 or ss >= 60:
            return -1
        return (mm * 60 + ss) * 1000 + mmm
    except Exception:
        return -1


class InspectorPanel(QWidget):
    """
    Right-side panel to inspect and edit selected clip's properties.

    Signals:
        apply_inout: (clip_id: int, start_ms: int, end_ms: int)
        rename_clip: (clip_id: int, new_label: str)
        set_in_from_player: () request main window to set in field from current player position
        set_out_from_player: () request main window to set out field from current player position
    """

    apply_inout = pyqtSignal(int, int, int)
    rename_clip = pyqtSignal(int, str)
    set_in_from_player = pyqtSignal()
    set_out_from_player = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._clip_id = None
        self._clip_duration_src_ms = None  # full source duration for validation (optional)
        self.init_ui()

    def init_ui(self):
        root = QVBoxLayout()
        self.setLayout(root)

        from utils.i18n_manager import i18n
        title = QLabel(i18n.t("inspector.title", "Inspector"))
        title.setStyleSheet("font-size: 12pt; font-weight: bold;")
        root.addWidget(title)

        # Basic group
        from utils.i18n_manager import i18n
        basic = QGroupBox(i18n.t("inspector.group_basic", "Basic"))
        b_l = QVBoxLayout()
        basic.setLayout(b_l)

        # Name
        row_name = QHBoxLayout()
        from utils.i18n_manager import i18n
        row_name.addWidget(QLabel(i18n.t("inspector.name", "Name:")))
        self.name_edit = QLineEdit()
        row_name.addWidget(self.name_edit)
        self.rename_btn = QPushButton("Rename")
        self.rename_btn.clicked.connect(self._on_rename)
        row_name.addWidget(self.rename_btn)
        b_l.addLayout(row_name)

        root.addWidget(basic)

        # In/Out group
        from utils.i18n_manager import i18n
        io = QGroupBox(i18n.t("inspector.group_io", "In/Out"))
        io_l = QVBoxLayout()
        io.setLayout(io_l)

        # In row
        row_in = QHBoxLayout()
        row_in.addWidget(QLabel("In (mm:ss.mmm):"))
        self.in_edit = QLineEdit("00:00.000")
        self.btn_in_from_player = QPushButton("Set from Current")
        self.btn_in_from_player.clicked.connect(self.set_in_from_player.emit)
        row_in.addWidget(self.in_edit)
        row_in.addWidget(self.btn_in_from_player)
        io_l.addLayout(row_in)

        # Out row
        row_out = QHBoxLayout()
        row_out.addWidget(QLabel("Out (mm:ss.mmm):"))
        self.out_edit = QLineEdit("00:00.000")
        self.btn_out_from_player = QPushButton("Set from Current")
        self.btn_out_from_player.clicked.connect(self.set_out_from_player.emit)
        row_out.addWidget(self.out_edit)
        row_out.addWidget(self.btn_out_from_player)
        io_l.addLayout(row_out)

        # Apply
        row_apply = QHBoxLayout()
        self.apply_btn = QPushButton("Apply to Clip")
        self.apply_btn.clicked.connect(self._on_apply)
        row_apply.addStretch()
        row_apply.addWidget(self.apply_btn)
        io_l.addLayout(row_apply)

        root.addWidget(io)
        root.addStretch()

    def set_clip(self, clip_id: int, label: str, start_ms: int, end_ms: int):
        self._clip_id = clip_id
        self.name_edit.setText(label or f"Clip {clip_id}")
        self.in_edit.setText(ms_to_mmssms(start_ms))
        self.out_edit.setText(ms_to_mmssms(end_ms))

    def set_in_from_ms(self, ms: int):
        self.in_edit.setText(ms_to_mmssms(ms))

    def set_out_from_ms(self, ms: int):
        self.out_edit.setText(ms_to_mmssms(ms))

    def _on_rename(self):
        if self._clip_id is None:
            return
        name = self.name_edit.text().strip()
        self.rename_clip.emit(self._clip_id, name)

    def _on_apply(self):
        if self._clip_id is None:
            return
        start_ms = mmssms_to_ms(self.in_edit.text().strip())
        end_ms = mmssms_to_ms(self.out_edit.text().strip())
        if start_ms < 0 or end_ms < 0 or end_ms < start_ms:
            # Simple guard; production can show message box
            return
        self.apply_inout.emit(self._clip_id, start_ms, end_ms)


