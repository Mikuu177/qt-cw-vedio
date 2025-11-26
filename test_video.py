"""
Test script to diagnose video playback issues
"""
import sys
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl

app = QApplication(sys.argv)

# Test 1: Check if video file exists
video_path = os.path.abspath("videos/unknown_2025.11.20-07.02_clip_1.mp4")
print(f"Video file path: {video_path}")
print(f"Video file exists: {os.path.exists(video_path)}")

# Test 2: Try to create media player
player = QMediaPlayer()
print(f"Media player created: {player}")

# Test 3: Check available services
print(f"Media player service: {player.service()}")
print(f"Availability: {player.availability()}")

# Test 4: Try to load the video
url = QUrl.fromLocalFile(video_path)
print(f"Video URL: {url.toString()}")
media = QMediaContent(url)
player.setMedia(media)

# Test 5: Check for errors
def on_error():
    error_code = player.error()
    error_string = player.errorString()
    print(f"ERROR: Code={error_code}, Message={error_string}")
    QMessageBox.critical(None, "Video Error", f"Cannot load video:\n{error_string}")

player.error.connect(on_error)

# Test 6: Check media status
def on_media_status_changed(status):
    status_names = {
        0: "UnknownMediaStatus",
        1: "NoMedia",
        2: "LoadingMedia",
        3: "LoadedMedia",
        4: "StalledMedia",
        5: "BufferingMedia",
        6: "BufferedMedia",
        7: "EndOfMedia",
        8: "InvalidMedia"
    }
    print(f"Media Status Changed: {status_names.get(status, 'Unknown')} ({status})")

player.mediaStatusChanged.connect(on_media_status_changed)

print("\nWaiting for media to load...")
print("If you see 'InvalidMedia' or error message, codec support may be missing.")
print("\nPress Ctrl+C to exit")

sys.exit(app.exec_())
