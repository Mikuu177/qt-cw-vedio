"""
Authentication Dialogs (PyQt5)
- LoginDialog
- RegisterDialog
- ForgotPasswordDialog

All dialogs use utils.auth_manager.AuthManager for operations.
"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QFormLayout, QComboBox
)
from PyQt5.QtCore import Qt

import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.auth_manager import AuthManager


class RegisterDialog(QDialog):
    def __init__(self, auth: AuthManager, parent=None):
        super().__init__(parent)
        self.auth = auth
        from utils.i18n_manager import i18n
        self.setWindowTitle(i18n.t("auth.register.title", "Register"))
        self.setModal(True)
        self.setMinimumWidth(420)
        
        layout = QVBoxLayout(self)
        form = QFormLayout()
        
        from utils.i18n_manager import i18n
        self.username_edit = QLineEdit(); self.username_edit.setPlaceholderText(i18n.t("auth.register.username", "Username (≥3)"))
        self.email_edit = QLineEdit(); self.email_edit.setPlaceholderText(i18n.t("auth.register.email", "Email (optional)"))
        self.password_edit = QLineEdit(); self.password_edit.setEchoMode(QLineEdit.Password); self.password_edit.setPlaceholderText(i18n.t("auth.register.password", "Password (≥6)"))
        self.confirm_edit = QLineEdit(); self.confirm_edit.setEchoMode(QLineEdit.Password); self.confirm_edit.setPlaceholderText(i18n.t("auth.register.confirm", "Confirm Password"))
        self.sec_q_edit = QLineEdit(); self.sec_q_edit.setPlaceholderText(i18n.t("auth.register.sec_q", "Security Question (optional)"))
        self.sec_a_edit = QLineEdit(); self.sec_a_edit.setEchoMode(QLineEdit.Password); self.sec_a_edit.setPlaceholderText(i18n.t("auth.register.sec_a", "Security Answer (optional)"))
        
        from utils.i18n_manager import i18n
        form.addRow(i18n.t("auth.register.username_label","Username:"), self.username_edit)
        form.addRow(i18n.t("auth.register.email_label","Email:"), self.email_edit)
        form.addRow(i18n.t("auth.register.password_label","Password:"), self.password_edit)
        form.addRow(i18n.t("auth.register.confirm_label","Confirm:"), self.confirm_edit)
        form.addRow(i18n.t("auth.register.sec_q_label","Security Question:"), self.sec_q_edit)
        form.addRow(i18n.t("auth.register.sec_a_label","Security Answer:"), self.sec_a_edit)
        layout.addLayout(form)
        
        btns = QHBoxLayout()
        btns.addStretch()
        from utils.i18n_manager import i18n
        self.btn_register = QPushButton(i18n.t("auth.register.btn_register", "Register"))
        self.btn_cancel = QPushButton(i18n.t("auth.register.btn_cancel", "Cancel"))
        btns.addWidget(self.btn_register)
        btns.addWidget(self.btn_cancel)
        layout.addLayout(btns)
        
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_register.clicked.connect(self.on_register)
    
    def on_register(self):
        u = self.username_edit.text().strip()
        e = self.email_edit.text().strip()
        p = self.password_edit.text()
        c = self.confirm_edit.text()
        q = self.sec_q_edit.text().strip()
        a = self.sec_a_edit.text()
        if p != c:
            from utils.i18n_manager import i18n
            QMessageBox.warning(self, i18n.t("auth.register.title","Register"), i18n.t("auth.register.password_mismatch","Passwords do not match"))
            return
        ok, msg = self.auth.register(u, p, e, q, a)
        if ok:
            QMessageBox.information(self, "成功", msg)
            self.accept()
        else:
            QMessageBox.warning(self, "失败", msg)


class ForgotPasswordDialog(QDialog):
    def __init__(self, auth: AuthManager, parent=None):
        super().__init__(parent)
        self.auth = auth
        from utils.i18n_manager import i18n
        self.setWindowTitle(i18n.t("auth.forgot.title", "Forgot Password"))
        self.setModal(True)
        self.setMinimumWidth(420)
        
        self.username_edit = QLineEdit(); self.username_edit.setPlaceholderText("用户名")
        self.question_label = QLabel("安全问题: (请输入用户名后点击获取)")
        self.answer_edit = QLineEdit(); self.answer_edit.setPlaceholderText("安全答案"); self.answer_edit.setEchoMode(QLineEdit.Password)
        self.new_pwd_edit = QLineEdit(); self.new_pwd_edit.setPlaceholderText("新密码 (≥6)"); self.new_pwd_edit.setEchoMode(QLineEdit.Password)
        
        layout = QVBoxLayout(self)
        form = QFormLayout()
        form.addRow("用户名:", self.username_edit)
        form.addRow("", self.question_label)
        form.addRow("答案:", self.answer_edit)
        form.addRow("新密码:", self.new_pwd_edit)
        layout.addLayout(form)
        
        btns = QHBoxLayout()
        self.btn_fetch = QPushButton("获取问题")
        self.btn_reset = QPushButton("重置密码")
        self.btn_cancel = QPushButton("取消")
        btns.addWidget(self.btn_fetch)
        btns.addStretch()
        btns.addWidget(self.btn_reset)
        btns.addWidget(self.btn_cancel)
        layout.addLayout(btns)
        
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_fetch.clicked.connect(self.on_fetch)
        self.btn_reset.clicked.connect(self.on_reset)
    
    def on_fetch(self):
        u = self.username_edit.text().strip()
        ok, q = self.auth.get_security_question(u)
        if ok:
            self.question_label.setText(f"安全问题: {q}")
        else:
            QMessageBox.warning(self, "失败", q)
    
    def on_reset(self):
        u = self.username_edit.text().strip()
        a = self.answer_edit.text()
        np = self.new_pwd_edit.text()
        ok, msg = self.auth.reset_password(u, a, np)
        if ok:
            QMessageBox.information(self, "成功", msg)
            self.accept()
        else:
            QMessageBox.warning(self, "失败", msg)


class LoginDialog(QDialog):
    def __init__(self, auth: AuthManager, parent=None):
        super().__init__(parent)
        self.auth = auth
        from utils.i18n_manager import i18n
        self.setWindowTitle(i18n.t("auth.login.title", "Login"))
        self.setModal(True)
        self.setMinimumWidth(380)
        
        layout = QVBoxLayout(self)
        form = QFormLayout()
        from utils.i18n_manager import i18n
        self.username_edit = QLineEdit(); self.username_edit.setPlaceholderText(i18n.t("auth.login.username", "Username"))
        self.password_edit = QLineEdit(); self.password_edit.setPlaceholderText(i18n.t("auth.login.password", "Password")); self.password_edit.setEchoMode(QLineEdit.Password)
        form.addRow("用户名:", self.username_edit)
        form.addRow("密码:", self.password_edit)
        layout.addLayout(form)
        
        row = QHBoxLayout()
        self.btn_login = QPushButton("登录")
        self.btn_register = QPushButton("注册...")
        self.btn_forgot = QPushButton("忘记密码...")
        self.btn_cancel = QPushButton("退出")
        row.addWidget(self.btn_login)
        row.addWidget(self.btn_register)
        row.addWidget(self.btn_forgot)
        row.addStretch()
        row.addWidget(self.btn_cancel)
        layout.addLayout(row)
        
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_login.clicked.connect(self.on_login)
        self.btn_register.clicked.connect(self.on_register)
        self.btn_forgot.clicked.connect(self.on_forgot)
        
        # UX: Enter to login
        self.username_edit.returnPressed.connect(self.on_login)
        self.password_edit.returnPressed.connect(self.on_login)
    
    def on_login(self):
        u = self.username_edit.text().strip()
        p = self.password_edit.text()
        ok, msg = self.auth.login(u, p)
        if ok:
            self.accept()
        else:
            QMessageBox.warning(self, "登录失败", msg)
    
    def on_register(self):
        dlg = RegisterDialog(self.auth, self)
        dlg.exec_()
    
    def on_forgot(self):
        dlg = ForgotPasswordDialog(self.auth, self)
        dlg.exec_()


