import sys
import os

# Add src to path
sys.path.insert(0, 'src')

print("="*50)
print("VIDEO PLAYER TEST")
print("="*50)

# Test PyQt5 import
try:
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtMultimedia import QMediaPlayer
    print("[OK] PyQt5 imported successfully")
except Exception as e:
    print(f"[ERROR] Failed to import PyQt5: {e}")
    sys.exit(1)

# Create app
app = QApplication(sys.argv)
print("[OK] QApplication created")

# Test video file
video_file = "videos/unknown_2025.11.20-07.02_clip_1.mp4"
print(f"\nChecking video file: {video_file}")
print(f"  Exists: {os.path.exists(video_file)}")
if os.path.exists(video_file):
    print(f"  Size: {os.path.getsize(video_file):,} bytes")
    print(f"  Abs path: {os.path.abspath(video_file)}")

# Import and create main window
try:
    from ui.main_window import MainWindow
    print("\n[OK] MainWindow imported")

    window = MainWindow()
    print("[OK] MainWindow created")
    print("\nCheck the GUI window now...")
    print("Look for debug messages above.")

    window.show()
    sys.exit(app.exec_())

except Exception as e:
    print(f"\n[ERROR] Failed to create window: {e}")
    import traceback
    traceback.print_exc()
