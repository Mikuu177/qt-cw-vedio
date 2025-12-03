"""
Simple Internationalization (i18n) Manager

- Loads language strings from JSON files in src/resources/
- Persists selected language using QSettings
- Provides i18n.t(key, default) helper for lookups with safe fallback

Supported languages: 'en', 'zh'
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional
from PyQt5.QtCore import QSettings


class _I18N:
    def __init__(self):
        self._settings = QSettings("XJCO2811", "VideoEditor")
        self._lang = self._load_saved_language()
        self._strings: Dict[str, Any] = {}
        self._load_strings()

    def _resources_dir(self) -> str:
        # src/utils/i18n_manager.py -> src/resources
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base, "resources")

    def _lang_file_path(self, lang: str) -> str:
        return os.path.join(self._resources_dir(), f"strings_{lang}.json")

    def _load_saved_language(self) -> str:
        lang = self._settings.value("language", type=str)
        if lang in ("en", "zh"):
            return lang
        # Default to English
        return "en"

    def _load_strings(self) -> None:
        self._strings = {}
        path = self._lang_file_path(self._lang)
        try:
            with open(path, "r", encoding="utf-8") as f:
                self._strings = json.load(f)
        except Exception:
            # Safe fallback: keep empty dict
            self._strings = {}

    def set_language(self, lang: str) -> None:
        if lang not in ("en", "zh"):
            return
        if lang == self._lang:
            return
        self._lang = lang
        self._settings.setValue("language", lang)
        self._load_strings()

    def get_language(self) -> str:
        return self._lang

    def _get_nested(self, data: Dict[str, Any], key: str) -> Optional[Any]:
        cur: Any = data
        for part in key.split('.'):
            if isinstance(cur, dict) and part in cur:
                cur = cur[part]
            else:
                return None
        return cur

    def t(self, key: str, default: Optional[str] = None) -> str:
        """
        Translate key to current language string.
        - key: dotted key path, e.g., 'menu.file'
        - default: fallback text when translation missing
        """
        val = self._get_nested(self._strings, key)
        if isinstance(val, str):
            return val
        return default if default is not None else key


# Singleton instance
i18n = _I18N()








