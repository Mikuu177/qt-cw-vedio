"""
SelectClipsDialog - choose a subset of timeline clips to merge/export

- Shows a checkable table of clips (follow timeline order)
- Supports Select All / None / Invert
- Supports optional custom ordering (Move Up/Down)
- Returns selected clips in current table order
"""
from typing import List
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
    QCheckBox, QWidget, QRadioButton
)
from PyQt5.QtCore import Qt
import os

# local imports
import sys
import os as _os
sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from video.timeline import TimelineClip
from utils.i18n_manager import i18n


class SelectClipsDialog(QDialog):
    def __init__(self, clips: List[TimelineClip], parent=None):
        super().__init__(parent)
        self.setWindowTitle(i18n.t("select.title", "Export Selected Clips"))
        self.setMinimumSize(700, 420)
        self._clips = clips[:]  # timeline order
        self._custom_order_enabled = False
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel(i18n.t("select.subtitle", "Select clips to merge/export"))
        title.setStyleSheet("font-size: 13pt; font-weight: bold;")
        layout.addWidget(title)

        # Order mode
        order_layout = QHBoxLayout()
        self.rb_order_timeline = QRadioButton(i18n.t("select.order_timeline", "Follow timeline order"))
        self.rb_order_custom = QRadioButton(i18n.t("select.order_custom", "Custom order"))
        self.rb_order_timeline.setChecked(True)
        self.rb_order_timeline.toggled.connect(self._on_order_mode_changed)
        order_layout.addWidget(self.rb_order_timeline)
        order_layout.addWidget(self.rb_order_custom)
        order_layout.addStretch()
        layout.addLayout(order_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            i18n.t("select.header_select", "Select"),
            i18n.t("select.header_name", "Name"),
            i18n.t("select.header_in", "In"),
            i18n.t("select.header_out", "Out"),
            i18n.t("select.header_duration", "Duration"),
            i18n.t("select.header_source", "Source")
        ])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self._populate_table()
        layout.addWidget(self.table)

        # Buttons row
        btns_layout = QHBoxLayout()
        self.btn_select_all = QPushButton(i18n.t("select.btn_select_all", "Select All"))
        self.btn_select_none = QPushButton(i18n.t("select.btn_select_none", "Select None"))
        self.btn_select_inv = QPushButton(i18n.t("select.btn_select_inv", "Invert"))
        self.btn_up = QPushButton(i18n.t("select.btn_move_up", "Move Up"))
        self.btn_down = QPushButton(i18n.t("select.btn_move_down", "Move Down"))

        self.btn_select_all.clicked.connect(self._on_select_all)
        self.btn_select_none.clicked.connect(self._on_select_none)
        self.btn_select_inv.clicked.connect(self._on_select_invert)
        self.btn_up.clicked.connect(self._on_move_up)
        self.btn_down.clicked.connect(self._on_move_down)

        btns_layout.addWidget(self.btn_select_all)
        btns_layout.addWidget(self.btn_select_none)
        btns_layout.addWidget(self.btn_select_inv)
        btns_layout.addStretch()
        btns_layout.addWidget(self.btn_up)
        btns_layout.addWidget(self.btn_down)
        layout.addLayout(btns_layout)

        # Footer
        footer = QHBoxLayout()
        footer.addStretch()
        self.btn_next = QPushButton(i18n.t("select.btn_next", "Next"))
        self.btn_cancel = QPushButton(i18n.t("select.btn_cancel", "Cancel"))
        self.btn_next.clicked.connect(self._on_next)
        self.btn_cancel.clicked.connect(self.reject)
        footer.addWidget(self.btn_next)
        footer.addWidget(self.btn_cancel)
        layout.addLayout(footer)

        self._update_buttons_state()

    def _populate_table(self):
        self.table.setRowCount(len(self._clips))
        for row, c in enumerate(self._clips):
            # Checkbox in column 0
            w = QCheckBox()
            w.setChecked(True)
            w.setStyleSheet("margin-left: 8px;")
            self.table.setCellWidget(row, 0, w)

            # Name
            name = c.label if c.label else os.path.basename(c.source_path)
            item_name = QTableWidgetItem(name)
            self._make_readonly(item_name)
            self.table.setItem(row, 1, item_name)

            # In
            self.table.setItem(row, 2, self._readonly_item(self._fmt_ms(c.start_time_ms)))
            # Out
            self.table.setItem(row, 3, self._readonly_item(self._fmt_ms(c.end_time_ms)))
            # Duration
            self.table.setItem(row, 4, self._readonly_item(self._fmt_ms(c.duration_ms)))
            # Source
            self.table.setItem(row, 5, self._readonly_item(os.path.basename(c.source_path)))

    @staticmethod
    def _fmt_ms(ms: int) -> str:
        ms = max(0, int(ms))
        s, milli = divmod(ms, 1000)
        m, sec = divmod(s, 60)
        return f"{m:02d}:{sec:02d}.{milli:03d}"

    @staticmethod
    def _make_readonly(item: QTableWidgetItem):
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

    @staticmethod
    def _readonly_item(text: str) -> QTableWidgetItem:
        it = QTableWidgetItem(text)
        it.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        return it

    def _on_select_all(self):
        for r in range(self.table.rowCount()):
            w = self.table.cellWidget(r, 0)
            if isinstance(w, QCheckBox):
                w.setChecked(True)

    def _on_select_none(self):
        for r in range(self.table.rowCount()):
            w = self.table.cellWidget(r, 0)
            if isinstance(w, QCheckBox):
                w.setChecked(False)

    def _on_select_invert(self):
        for r in range(self.table.rowCount()):
            w = self.table.cellWidget(r, 0)
            if isinstance(w, QCheckBox):
                w.setChecked(not w.isChecked())

    def _on_order_mode_changed(self, checked: bool):
        self._custom_order_enabled = self.rb_order_custom.isChecked()
        self._update_buttons_state()

    def _update_buttons_state(self):
        self.btn_up.setEnabled(self._custom_order_enabled)
        self.btn_down.setEnabled(self._custom_order_enabled)

    def _on_move_up(self):
        if not self._custom_order_enabled:
            return
        row = self.table.currentRow()
        if row <= 0:
            return
        self._swap_rows(row, row - 1)
        self.table.selectRow(row - 1)

    def _on_move_down(self):
        if not self._custom_order_enabled:
            return
        row = self.table.currentRow()
        if row < 0 or row >= self.table.rowCount() - 1:
            return
        self._swap_rows(row, row + 1)
        self.table.selectRow(row + 1)

    def _swap_rows(self, r1: int, r2: int):
        # Swap in UI and in self._clips to keep mapping
        self._clips[r1], self._clips[r2] = self._clips[r2], self._clips[r1]
        for col in range(self.table.columnCount()):
            if col == 0:
                # swap checkbox state
                w1 = self.table.cellWidget(r1, 0)
                w2 = self.table.cellWidget(r2, 0)
                if isinstance(w1, QCheckBox) and isinstance(w2, QCheckBox):
                    state1 = w1.isChecked()
                    state2 = w2.isChecked()
                    w1.setChecked(state2)
                    w2.setChecked(state1)
            else:
                i1 = self.table.item(r1, col)
                i2 = self.table.item(r2, col)
                t1 = i1.text() if i1 else ""
                t2 = i2.text() if i2 else ""
                if i1:
                    i1.setText(t2)
                if i2:
                    i2.setText(t1)

    def _on_next(self):
        # Must have at least one selected
        selected = []
        for r, c in enumerate(self._clips):
            w = self.table.cellWidget(r, 0)
            checked = isinstance(w, QCheckBox) and w.isChecked()
            if checked:
                selected.append(c)
        if not selected:
            # simple feedback: keep dialog open
            self.setWindowTitle(i18n.t("select.title","Export Selected Clips") + " - " + i18n.t("select.please_select","(please select at least one)"))
            return
        self._selection = selected
        self._custom_order = self._custom_order_enabled
        self.accept()

    def get_selection(self) -> List[TimelineClip]:
        return getattr(self, "_selection", [])

    def is_custom_order(self) -> bool:
        return getattr(self, "_custom_order", False)


