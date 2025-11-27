"""
FFmpeg Processor - Video Editing Operations

This module handles video processing operations using FFmpeg:
- Trimming/cutting video segments
- Concatenating multiple clips
- Exporting with quality settings
"""

import subprocess
import os
import tempfile
from typing import List, Optional, Tuple
from PyQt5.QtCore import QObject, pyqtSignal, QThread


class FFmpegProcessor(QObject):
    """Handles FFmpeg video processing operations."""

    # Signals for progress tracking
    progress_updated = pyqtSignal(int)  # Progress percentage (0-100)
    process_completed = pyqtSignal(bool, str)  # Success, output_path or error message
    process_started = pyqtSignal()

    # Quality presets
    QUALITY_HIGH = "high"
    QUALITY_MEDIUM = "medium"
    QUALITY_LOW = "low"

    QUALITY_SETTINGS = {
        QUALITY_HIGH: {
            "crf": "18",
            "preset": "medium",
            "scale": None,  # Keep original resolution
            "bitrate_audio": "192k"
        },
        QUALITY_MEDIUM: {
            "crf": "23",
            "preset": "medium",
            "scale": "1280:720",  # 720p
            "bitrate_audio": "128k"
        },
        QUALITY_LOW: {
            "crf": "28",
            "preset": "fast",
            "scale": "854:480",  # 480p
            "bitrate_audio": "96k"
        }
    }

    def __init__(self):
        super().__init__()
        self.process = None
        self.is_cancelled = False

    @staticmethod
    def check_ffmpeg_available() -> bool:
        """Check if FFmpeg is available in system PATH."""
        try:
            result = subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def trim_video(
        self,
        input_path: str,
        output_path: str,
        start_time_ms: int,
        end_time_ms: int,
        quality: str = QUALITY_HIGH
    ):
        """
        Trim a video segment.

        Args:
            input_path: Source video file
            output_path: Output file path
            start_time_ms: Start time in milliseconds
            end_time_ms: End time in milliseconds
            quality: Quality preset (high/medium/low)
        """
        self.is_cancelled = False
        self.process_started.emit()

        # Convert milliseconds to seconds
        start_sec = start_time_ms / 1000.0
        duration_sec = (end_time_ms - start_time_ms) / 1000.0

        # Get quality settings
        settings = self.QUALITY_SETTINGS.get(quality, self.QUALITY_SETTINGS[self.QUALITY_HIGH])

        # Build FFmpeg command
        cmd = [
            "ffmpeg",
            "-i", input_path,
            "-ss", str(start_sec),
            "-t", str(duration_sec),
            "-c:v", "libx264",
            "-crf", settings["crf"],
            "-preset", settings["preset"],
            "-c:a", "aac",
            "-b:a", settings["bitrate_audio"],
        ]

        # Add scaling if specified
        if settings["scale"]:
            cmd.extend(["-vf", f"scale={settings['scale']}"])

        cmd.extend(["-y", output_path])  # -y to overwrite

        print(f"[FFmpeg] Executing: {' '.join(cmd)}")

        try:
            # Run FFmpeg process
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            # Monitor progress (FFmpeg outputs to stderr)
            for line in self.process.stderr:
                if self.is_cancelled:
                    self.process.terminate()
                    self.process_completed.emit(False, "Cancelled by user")
                    return

                # Parse progress from FFmpeg output
                # FFmpeg outputs: frame=X fps=Y size=Z time=HH:MM:SS.mmm
                if "time=" in line:
                    # Simple progress estimation
                    # (In production, parse actual time and calculate percentage)
                    pass

            self.process.wait()

            if self.process.returncode == 0 and os.path.exists(output_path):
                self.progress_updated.emit(100)
                self.process_completed.emit(True, output_path)
            else:
                error_msg = f"FFmpeg failed with return code {self.process.returncode}"
                self.process_completed.emit(False, error_msg)

        except Exception as e:
            error_msg = f"Error running FFmpeg: {str(e)}"
            print(f"[FFmpeg] {error_msg}")
            self.process_completed.emit(False, error_msg)

    def concatenate_clips(
        self,
        clips: List[Tuple[str, int, int]],  # [(path, start_ms, end_ms), ...]
        output_path: str,
        quality: str = QUALITY_HIGH
    ):
        """
        Concatenate multiple video clips.

        Args:
            clips: List of (file_path, start_ms, end_ms) tuples
            output_path: Output file path
            quality: Quality preset
        """
        self.is_cancelled = False
        self.process_started.emit()

        try:
            # Create temporary trimmed clips
            temp_dir = tempfile.mkdtemp()
            temp_clips = []
            concat_file = os.path.join(temp_dir, "concat_list.txt")

            print(f"[FFmpeg] Processing {len(clips)} clips...")

            # Step 1: Trim each clip
            for idx, (path, start_ms, end_ms) in enumerate(clips):
                if self.is_cancelled:
                    self.process_completed.emit(False, "Cancelled by user")
                    return

                temp_clip = os.path.join(temp_dir, f"clip_{idx}.mp4")
                temp_clips.append(temp_clip)

                # Trim this clip
                self._trim_clip_sync(path, temp_clip, start_ms, end_ms, quality)

                # Update progress
                progress = int((idx + 1) / len(clips) * 80)  # 0-80%
                self.progress_updated.emit(progress)

            # Step 2: Create concat file
            with open(concat_file, 'w') as f:
                for clip in temp_clips:
                    f.write(f"file '{clip}'\n")

            # Step 3: Concatenate using concat demuxer (fastest)
            cmd = [
                "ffmpeg",
                "-f", "concat",
                "-safe", "0",
                "-i", concat_file,
                "-c", "copy",  # Stream copy (fast, no re-encoding)
                "-y", output_path
            ]

            print(f"[FFmpeg] Concatenating clips: {' '.join(cmd)}")

            result = subprocess.run(
                cmd,
                capture_output=True,
                universal_newlines=True,
                timeout=300  # 5 min timeout
            )

            # Cleanup temp files
            for clip in temp_clips:
                if os.path.exists(clip):
                    os.remove(clip)
            if os.path.exists(concat_file):
                os.remove(concat_file)
            os.rmdir(temp_dir)

            if result.returncode == 0 and os.path.exists(output_path):
                self.progress_updated.emit(100)
                self.process_completed.emit(True, output_path)
            else:
                error_msg = f"Concatenation failed: {result.stderr}"
                self.process_completed.emit(False, error_msg)

        except Exception as e:
            error_msg = f"Error concatenating clips: {str(e)}"
            print(f"[FFmpeg] {error_msg}")
            self.process_completed.emit(False, error_msg)

    def _trim_clip_sync(
        self,
        input_path: str,
        output_path: str,
        start_ms: int,
        end_ms: int,
        quality: str
    ):
        """Synchronously trim a clip (used internally for concatenation)."""
        start_sec = start_ms / 1000.0
        duration_sec = (end_ms - start_ms) / 1000.0

        settings = self.QUALITY_SETTINGS.get(quality, self.QUALITY_SETTINGS[self.QUALITY_HIGH])

        cmd = [
            "ffmpeg",
            "-i", input_path,
            "-ss", str(start_sec),
            "-t", str(duration_sec),
            "-c:v", "libx264",
            "-crf", settings["crf"],
            "-preset", settings["preset"],
            "-c:a", "aac",
            "-b:a", settings["bitrate_audio"],
            "-y", output_path
        ]

        if settings["scale"]:
            cmd.extend(["-vf", f"scale={settings['scale']}"])

        result = subprocess.run(cmd, capture_output=True, timeout=60)

        if result.returncode != 0:
            raise RuntimeError(f"Failed to trim clip: {result.stderr.decode()}")

    def cancel(self):
        """Cancel the current operation."""
        self.is_cancelled = True
        if self.process and self.process.poll() is None:
            self.process.terminate()


class FFmpegWorker(QThread):
    """Worker thread for running FFmpeg operations without blocking UI."""

    def __init__(self, processor: FFmpegProcessor, operation: str, **kwargs):
        super().__init__()
        self.processor = processor
        self.operation = operation
        self.kwargs = kwargs

    def run(self):
        """Execute the FFmpeg operation in thread."""
        if self.operation == "trim":
            self.processor.trim_video(**self.kwargs)
        elif self.operation == "concatenate":
            self.processor.concatenate_clips(**self.kwargs)


# Utility functions
def get_video_info(file_path: str) -> Optional[dict]:
    """
    Get video metadata using ffprobe.

    Returns:
        dict with keys: duration_ms, width, height, fps, codec
        None if failed
    """
    try:
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            file_path
        ]

        result = subprocess.run(cmd, capture_output=True, timeout=10)

        if result.returncode != 0:
            return None

        import json
        data = json.loads(result.stdout.decode())

        # Find video stream
        video_stream = None
        for stream in data.get("streams", []):
            if stream.get("codec_type") == "video":
                video_stream = stream
                break

        if not video_stream:
            return None

        # Extract info
        duration_ms = int(float(data["format"]["duration"]) * 1000)
        width = video_stream.get("width", 0)
        height = video_stream.get("height", 0)

        # Parse FPS (can be in various formats like "30/1")
        fps_str = video_stream.get("r_frame_rate", "30/1")
        num, denom = fps_str.split("/")
        fps = float(num) / float(denom)

        codec = video_stream.get("codec_name", "unknown")

        return {
            "duration_ms": duration_ms,
            "width": width,
            "height": height,
            "fps": fps,
            "codec": codec
        }

    except Exception as e:
        print(f"[FFprobe] Error getting video info: {e}")
        return None


def format_time(milliseconds: int) -> str:
    """Format milliseconds as HH:MM:SS."""
    seconds = milliseconds // 1000
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"
