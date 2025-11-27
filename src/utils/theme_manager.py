"""
Theme Manager - High Contrast Mode for Accessibility

Provides theme switching between normal and high contrast modes
to improve accessibility for visually impaired users.

Complies with WCAG 2.1 Level AA contrast requirements (4.5:1 for text, 3:1 for UI components)
"""

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSettings


class ThemeManager:
    """Manages application themes and high contrast mode."""

    # Theme names
    THEME_NORMAL = "normal"
    THEME_HIGH_CONTRAST = "high_contrast"

    # Normal theme stylesheet
    NORMAL_THEME = """
    QMainWindow {
        background-color: #f5f5f5;
    }

    QPushButton {
        background-color: #e0e0e0;
        color: #000000;
        border: 1px solid #cccccc;
        border-radius: 4px;
        padding: 6px 12px;
        font-size: 10pt;
    }

    QPushButton:hover {
        background-color: #d0d0d0;
        border: 1px solid #999999;
    }

    QPushButton:pressed {
        background-color: #c0c0c0;
    }

    QPushButton:disabled {
        background-color: #f0f0f0;
        color: #999999;
    }

    QPushButton:focus {
        border: 2px solid #0078d4;
    }

    QSlider::groove:horizontal {
        border: 1px solid #999999;
        height: 6px;
        background: #e0e0e0;
        margin: 2px 0;
        border-radius: 3px;
    }

    QSlider::handle:horizontal {
        background: #0078d4;
        border: 1px solid #005a9e;
        width: 16px;
        margin: -5px 0;
        border-radius: 8px;
    }

    QSlider::handle:horizontal:hover {
        background: #006cc1;
    }

    QComboBox {
        background-color: #ffffff;
        color: #000000;
        border: 1px solid #cccccc;
        border-radius: 4px;
        padding: 4px 8px;
        min-width: 60px;
    }

    QComboBox:hover {
        border: 1px solid #999999;
    }

    QComboBox:focus {
        border: 2px solid #0078d4;
    }

    QComboBox::drop-down {
        border: none;
    }

    QLabel {
        color: #000000;
        font-size: 10pt;
    }

    QStatusBar {
        background-color: #f0f0f0;
        color: #000000;
        border-top: 1px solid #cccccc;
    }

    QMenuBar {
        background-color: #ffffff;
        color: #000000;
        border-bottom: 1px solid #cccccc;
    }

    QMenuBar::item {
        background-color: transparent;
        padding: 4px 8px;
    }

    QMenuBar::item:selected {
        background-color: #e0e0e0;
    }

    QMenu {
        background-color: #ffffff;
        color: #000000;
        border: 1px solid #cccccc;
    }

    QMenu::item:selected {
        background-color: #0078d4;
        color: #ffffff;
    }
    """

    # High contrast theme stylesheet
    # Follows WCAG 2.1 Level AAA guidelines (7:1 contrast ratio for text)
    HIGH_CONTRAST_THEME = """
    QMainWindow {
        background-color: #000000;
    }

    QPushButton {
        background-color: #000000;
        color: #FFFF00;
        border: 3px solid #FFFFFF;
        border-radius: 4px;
        padding: 8px 14px;
        font-size: 11pt;
        font-weight: bold;
    }

    QPushButton:hover {
        background-color: #1a1a1a;
        border: 3px solid #FFFF00;
    }

    QPushButton:pressed {
        background-color: #333333;
        border: 3px solid #00FF00;
    }

    QPushButton:disabled {
        background-color: #000000;
        color: #808080;
        border: 3px solid #404040;
    }

    QPushButton:focus {
        border: 4px solid #00FFFF;
        outline: none;
    }

    QSlider::groove:horizontal {
        border: 2px solid #FFFFFF;
        height: 8px;
        background: #000000;
        margin: 2px 0;
        border-radius: 4px;
    }

    QSlider::handle:horizontal {
        background: #FFFF00;
        border: 3px solid #FFFFFF;
        width: 20px;
        margin: -7px 0;
        border-radius: 10px;
    }

    QSlider::handle:horizontal:hover {
        background: #00FF00;
    }

    QSlider::handle:horizontal:focus {
        border: 3px solid #00FFFF;
    }

    QComboBox {
        background-color: #000000;
        color: #FFFF00;
        border: 3px solid #FFFFFF;
        border-radius: 4px;
        padding: 6px 10px;
        min-width: 70px;
        font-size: 11pt;
        font-weight: bold;
    }

    QComboBox:hover {
        border: 3px solid #FFFF00;
    }

    QComboBox:focus {
        border: 4px solid #00FFFF;
    }

    QComboBox::drop-down {
        border: none;
        width: 20px;
    }

    QComboBox::down-arrow {
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 8px solid #FFFF00;
    }

    QComboBox QAbstractItemView {
        background-color: #000000;
        color: #FFFF00;
        border: 3px solid #FFFFFF;
        selection-background-color: #FFFF00;
        selection-color: #000000;
        font-weight: bold;
    }

    QLabel {
        color: #FFFFFF;
        font-size: 11pt;
        font-weight: bold;
    }

    QStatusBar {
        background-color: #000000;
        color: #FFFF00;
        border-top: 3px solid #FFFFFF;
        font-size: 11pt;
        font-weight: bold;
    }

    QMenuBar {
        background-color: #000000;
        color: #FFFF00;
        border-bottom: 3px solid #FFFFFF;
        font-weight: bold;
    }

    QMenuBar::item {
        background-color: transparent;
        padding: 6px 10px;
    }

    QMenuBar::item:selected {
        background-color: #FFFF00;
        color: #000000;
    }

    QMenu {
        background-color: #000000;
        color: #FFFF00;
        border: 3px solid #FFFFFF;
        font-weight: bold;
    }

    QMenu::item {
        padding: 6px 20px;
    }

    QMenu::item:selected {
        background-color: #FFFF00;
        color: #000000;
    }

    /* Focus indicators for accessibility */
    *:focus {
        outline: none;
    }

    /* Ensure text remains readable */
    QLineEdit, QTextEdit, QPlainTextEdit {
        background-color: #000000;
        color: #FFFFFF;
        border: 3px solid #FFFFFF;
        font-size: 11pt;
        font-weight: bold;
    }

    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
        border: 4px solid #00FFFF;
    }
    """

    def __init__(self, app: QApplication):
        """
        Initialize theme manager.

        Args:
            app: QApplication instance
        """
        self.app = app
        self.settings = QSettings("XJCO2811", "VideoEditor")
        self.current_theme = self.THEME_NORMAL

        # Load saved theme preference
        saved_theme = self.settings.value("theme", self.THEME_NORMAL)
        self.apply_theme(saved_theme)

    def apply_theme(self, theme_name: str):
        """
        Apply a theme to the application.

        Args:
            theme_name: Either THEME_NORMAL or THEME_HIGH_CONTRAST
        """
        if theme_name == self.THEME_NORMAL:
            self.app.setStyleSheet(self.NORMAL_THEME)
            self.current_theme = self.THEME_NORMAL
            print("[Theme] Applied normal theme")

        elif theme_name == self.THEME_HIGH_CONTRAST:
            self.app.setStyleSheet(self.HIGH_CONTRAST_THEME)
            self.current_theme = self.THEME_HIGH_CONTRAST
            print("[Theme] Applied high contrast theme (WCAG 2.1 Level AAA)")

        else:
            print(f"[Theme] Unknown theme: {theme_name}, using normal theme")
            self.app.setStyleSheet(self.NORMAL_THEME)
            self.current_theme = self.THEME_NORMAL

        # Save preference
        self.settings.setValue("theme", self.current_theme)

    def toggle_high_contrast(self):
        """Toggle between normal and high contrast themes."""
        if self.current_theme == self.THEME_NORMAL:
            self.apply_theme(self.THEME_HIGH_CONTRAST)
        else:
            self.apply_theme(self.THEME_NORMAL)

    def is_high_contrast(self) -> bool:
        """Check if high contrast mode is active."""
        return self.current_theme == self.THEME_HIGH_CONTRAST

    def get_current_theme(self) -> str:
        """Get the name of the current theme."""
        return self.current_theme


# Accessibility helper functions
def get_contrast_ratio(foreground_hex: str, background_hex: str) -> float:
    """
    Calculate contrast ratio between two colors.

    Args:
        foreground_hex: Foreground color (hex: #RRGGBB)
        background_hex: Background color (hex: #RRGGBB)

    Returns:
        Contrast ratio (1.0 to 21.0)

    Reference: WCAG 2.1 contrast ratio formula
    """
    def hex_to_rgb(hex_color: str) -> tuple:
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def get_relative_luminance(rgb: tuple) -> float:
        """Calculate relative luminance (WCAG formula)."""
        r, g, b = [x / 255.0 for x in rgb]

        # Apply gamma correction
        r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
        g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
        b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4

        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    fg_rgb = hex_to_rgb(foreground_hex)
    bg_rgb = hex_to_rgb(background_hex)

    l1 = get_relative_luminance(fg_rgb)
    l2 = get_relative_luminance(bg_rgb)

    # Ensure L1 is the lighter color
    if l1 < l2:
        l1, l2 = l2, l1

    contrast = (l1 + 0.05) / (l2 + 0.05)
    return contrast


def meets_wcag_aa(foreground_hex: str, background_hex: str, large_text: bool = False) -> bool:
    """
    Check if color combination meets WCAG 2.1 Level AA.

    Args:
        foreground_hex: Foreground color
        background_hex: Background color
        large_text: True if text is ≥18pt or bold ≥14pt

    Returns:
        True if meets WCAG AA requirements
    """
    ratio = get_contrast_ratio(foreground_hex, background_hex)

    if large_text:
        return ratio >= 3.0  # AA for large text
    else:
        return ratio >= 4.5  # AA for normal text


def meets_wcag_aaa(foreground_hex: str, background_hex: str, large_text: bool = False) -> bool:
    """
    Check if color combination meets WCAG 2.1 Level AAA.

    Args:
        foreground_hex: Foreground color
        background_hex: Background color
        large_text: True if text is ≥18pt or bold ≥14pt

    Returns:
        True if meets WCAG AAA requirements
    """
    ratio = get_contrast_ratio(foreground_hex, background_hex)

    if large_text:
        return ratio >= 4.5  # AAA for large text
    else:
        return ratio >= 7.0  # AAA for normal text


# Testing
if __name__ == "__main__":
    # Test contrast ratios
    print("High Contrast Theme Tests:")
    print(f"Yellow on Black: {get_contrast_ratio('#FFFF00', '#000000'):.2f}:1")
    print(f"White on Black: {get_contrast_ratio('#FFFFFF', '#000000'):.2f}:1")
    print(f"Cyan on Black: {get_contrast_ratio('#00FFFF', '#000000'):.2f}:1")
    print(f"Green on Black: {get_contrast_ratio('#00FF00', '#000000'):.2f}:1")

    print("\nWCAG Compliance:")
    print(f"Yellow/Black AA: {meets_wcag_aa('#FFFF00', '#000000')}")
    print(f"Yellow/Black AAA: {meets_wcag_aaa('#FFFF00', '#000000')}")
    print(f"White/Black AA: {meets_wcag_aa('#FFFFFF', '#000000')}")
    print(f"White/Black AAA: {meets_wcag_aaa('#FFFFFF', '#000000')}")
