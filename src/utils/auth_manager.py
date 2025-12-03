"""
Auth Manager - Simple local authentication with SQLite + PBKDF2

Features:
- Register (username unique)
- Login (username/password)
- Forgot password via security question/answer
- Optional remember_me (persist last user)

Security notes:
- Passwords hashed with PBKDF2-HMAC-SHA256 + per-user random salt
- iterations=200_000 (configurable)
- Constant-time verify
"""
from __future__ import annotations

import os
import sqlite3
import secrets
import hashlib
import hmac
from dataclasses import dataclass
from typing import Optional, Tuple

try:
    # Prefer Qt path for per-user app data
    from PyQt5.QtCore import QStandardPaths
    def _default_db_path() -> str:
        base = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation) or os.path.expanduser("~/.qt_cw_vedio")
        os.makedirs(base, exist_ok=True)
        return os.path.join(base, "auth.db")
except Exception:
    def _default_db_path() -> str:
        base = os.path.join(os.path.expanduser("~"), ".qt_cw_vedio")
        os.makedirs(base, exist_ok=True)
        return os.path.join(base, "auth.db")


@dataclass
class User:
    id: int
    username: str
    email: str


class AuthManager:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or _default_db_path()
        self._ensure_schema()
        self.current_user: Optional[User] = None
        # Config
        self._iterations = 200_000
        self._salt_len = 16

    # ------------------ DB ------------------
    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _ensure_schema(self):
        con = self._connect()
        try:
            cur = con.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT,
                    password_hash BLOB NOT NULL,
                    salt BLOB NOT NULL,
                    iterations INTEGER NOT NULL,
                    sec_question TEXT,
                    sec_answer_hash BLOB
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS meta (
                    k TEXT PRIMARY KEY,
                    v TEXT
                )
                """
            )
            con.commit()
        finally:
            con.close()

    # ------------------ Crypto helpers ------------------
    def _hash_password(self, password: str, salt: Optional[bytes] = None, iterations: Optional[int] = None) -> Tuple[bytes, bytes, int]:
        if salt is None:
            salt = secrets.token_bytes(self._salt_len)
        iters = iterations or self._iterations
        dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iters)
        return dk, salt, iters

    def _hash_answer(self, answer: str, salt: bytes, iterations: int) -> bytes:
        return hashlib.pbkdf2_hmac("sha256", answer.encode("utf-8"), salt, iterations)

    # ------------------ API ------------------
    def register(self, username: str, password: str, email: str = "", sec_question: str = "", sec_answer: str = "") -> Tuple[bool, str]:
        username = (username or "").strip()
        if not username or not password:
            return False, "用户名和密码不能为空"
        if len(username) < 3:
            return False, "用户名至少 3 个字符"
        if len(password) < 6:
            return False, "密码至少 6 个字符"
        con = self._connect()
        try:
            cur = con.cursor()
            try:
                # Check unique
                cur.execute("SELECT id FROM users WHERE username=?", (username,))
                if cur.fetchone():
                    return False, "该用户名已被注册"
                pwd_hash, salt, iters = self._hash_password(password)
                ans_hash = None
                if sec_question and sec_answer:
                    ans_hash = self._hash_answer(sec_answer.strip(), salt, iters)
                cur.execute(
                    "INSERT INTO users (username, email, password_hash, salt, iterations, sec_question, sec_answer_hash) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (username, email.strip(), pwd_hash, salt, iters, sec_question.strip(), ans_hash)
                )
                con.commit()
                return True, "注册成功"
            except sqlite3.IntegrityError:
                return False, "该用户名已被注册"
        finally:
            con.close()

    def login(self, username: str, password: str) -> Tuple[bool, str]:
        username = (username or "").strip()
        if not username or not password:
            return False, "请输入用户名和密码"
        con = self._connect()
        try:
            cur = con.cursor()
            cur.execute("SELECT id, email, password_hash, salt, iterations FROM users WHERE username=?", (username,))
            row = cur.fetchone()
            if not row:
                return False, "用户不存在"
            uid, email, stored_hash, salt, iters = row
            calc_hash, _, _ = self._hash_password(password, salt, iters)
            if hmac.compare_digest(calc_hash, stored_hash):
                self.current_user = User(id=uid, username=username, email=email or "")
                return True, "登录成功"
            return False, "密码不正确"
        finally:
            con.close()

    def get_security_question(self, username: str) -> Tuple[bool, str]:
        con = self._connect()
        try:
            cur = con.cursor()
            cur.execute("SELECT sec_question FROM users WHERE username=?", (username.strip(),))
            row = cur.fetchone()
            if not row or not row[0]:
                return False, "未设置安全问题，无法找回"
            return True, row[0]
        finally:
            con.close()

    def reset_password(self, username: str, answer: str, new_password: str) -> Tuple[bool, str]:
        if len(new_password) < 6:
            return False, "新密码至少 6 个字符"
        con = self._connect()
        try:
            cur = con.cursor()
            cur.execute("SELECT id, password_hash, salt, iterations, sec_answer_hash FROM users WHERE username=?", (username.strip(),))
            row = cur.fetchone()
            if not row:
                return False, "用户不存在"
            uid, _, salt, iters, ans_hash = row
            if not ans_hash:
                return False, "未设置安全问题，无法找回"
            calc_ans = self._hash_answer(answer.strip(), salt, iters)
            if not hmac.compare_digest(calc_ans, ans_hash):
                return False, "安全答案不正确"
            # Update password
            new_hash, new_salt, new_iters = self._hash_password(new_password)
            cur.execute("UPDATE users SET password_hash=?, salt=?, iterations=? WHERE id=?", (new_hash, new_salt, new_iters, uid))
            con.commit()
            return True, "密码已重置"
        finally:
            con.close()

    def logout(self):
        self.current_user = None



