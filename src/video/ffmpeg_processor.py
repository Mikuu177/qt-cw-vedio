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
        Trim a video segment and report real-time progress.
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
            "-y", output_path
        ]
        print(f"[FFmpeg][Trim] Executing: {' '.join(cmd)}", flush=True)

        try:
            # Run FFmpeg process (stream stderr for progress)
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            # Estimate total duration in seconds for progress
            total_sec = max(0.01, (end_time_ms - start_time_ms) / 1000.0)

            def _parse_ff_time(s: str) -> float:
                import re
                m = re.search(r"time=(\d+):(\d+):(\d+\.?\d*)", s)
                if not m:
                    return -1.0
                hh = int(m.group(1)); mm = int(m.group(2)); ss = float(m.group(3))
                return hh * 3600.0 + mm * 60.0 + ss

            for line in self.process.stderr:
                if self.is_cancelled:
                    self.process.terminate()
                    print("[FFmpeg][Trim] Cancelled by user", flush=True)
                    self.process_completed.emit(False, "Cancelled by user")
                    return

                # Echo stderr for debugging
                try:
                    print(f"[FFmpeg][Trim][stderr] {line.strip()}", flush=True)
                except Exception:
                    pass

                # Parse progress from FFmpeg output (time=HH:MM:SS.mmm)
                if "time=" in line:
                    cur = _parse_ff_time(line)
                    if cur >= 0:
                        pct = int(min(cur / total_sec * 100.0, 99))
                        self.progress_updated.emit(pct)
                        print(f"[FFmpeg][Trim][progress] {pct}%", flush=True)

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
        quality: str = QUALITY_HIGH,
        transitions_enabled: bool = False,
        transition_ms: int = 500
    ):
        """
        Concatenate multiple video clips. Progress: trim stage 0→60%, concat stage 60→99%, finish 100%.
        """
        self.is_cancelled = False
        self.process_started.emit()

        try:
            # Create temporary trimmed clips
            temp_dir = tempfile.mkdtemp()
            temp_clips = []
            durations_sec = []
            concat_file = os.path.join(temp_dir, "concat_list.txt")

            print(f"[FFmpeg] Processing {len(clips)} clips...", flush=True)

            # Step 1: Trim each clip
            for idx, (path, start_ms, end_ms) in enumerate(clips):
                if self.is_cancelled:
                    self.process_completed.emit(False, "Cancelled by user")
                    return

                temp_clip = os.path.join(temp_dir, f"clip_{idx}.mp4")
                temp_clips.append(temp_clip)

                # Trim this clip (re-encode with selected quality)
                self._trim_clip_sync(path, temp_clip, start_ms, end_ms, quality)

                # Record duration in seconds
                durations_sec.append(max(0.01, (end_ms - start_ms) / 1000.0))

                # Update progress (0→60%)
                progress = int((idx + 1) / max(1, len(clips)) * 60)
                self.progress_updated.emit(progress)

            # Step 2: Concatenate
            if not transitions_enabled or len(temp_clips) <= 1:
                # Use concat demuxer (fast stream copy) and parse progress
                with open(concat_file, 'w') as f:
                    for clip in temp_clips:
                        f.write(f"file '{clip}'\n")

                cmd = [
                    "ffmpeg",
                    "-f", "concat",
                    "-safe", "0",
                    "-i", concat_file,
                    "-c", "copy",
                    "-y", output_path
                ]
                print(f"[FFmpeg] Concatenating clips: {' '.join(cmd)}", flush=True)

                # Total seconds for concat stage
                acc_total = max(0.01, sum(durations_sec))

                def _parse_ff_time(s: str) -> float:
                    import re
                    m = re.search(r"time=(\d+):(\d+):(\d+\.?\d*)", s)
                    if not m:
                        return -1.0
                    hh = int(m.group(1)); mm = int(m.group(2)); ss = float(m.group(3))
                    return hh * 3600.0 + mm * 60.0 + ss

                self.process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
                for line in self.process.stderr:
                    if self.is_cancelled:
                        self.process.terminate()
                        self.process_completed.emit(False, "Cancelled by user")
                        return
                    try:
                        print(f"[FFmpeg][Concat][stderr] {line.strip()}", flush=True)
                    except Exception:
                        pass
                    if "time=" in line:
                        cur = _parse_ff_time(line)
                        if cur >= 0:
                            pct = 60 + int(min(cur / acc_total, 1.0) * 39)
                            self.progress_updated.emit(min(pct, 99))
                self.process.wait()
                result_code = self.process.returncode

            else:
                # Build filter_complex for xfade/acrossfade progressive chaining
                td = max(0.05, transition_ms / 1000.0)
                # Inputs
                cmd = ["ffmpeg"]
                for clip in temp_clips:
                    cmd.extend(["-i", clip])

                # Detect audio presence; if any clip lacks audio -> degrade to video-only xfade
                def _has_audio(path: str) -> bool:
                    try:
                        probe = subprocess.run([
                            "ffprobe", "-v", "error", "-select_streams", "a:0",
                            "-show_entries", "stream=codec_type", "-of", "csv=p=0", path
                        ], capture_output=True, timeout=10)
                        out = (probe.stdout or b"").decode(errors="ignore").strip()
                        return "audio" in out.lower()
                    except Exception:
                        return False

                has_audio_all = all(_has_audio(p) for p in temp_clips)

                filter_lines = []
                out_v = "[0:v]"
                out_a = "[0:a]" if has_audio_all else None
                acc_dur = durations_sec[0]
                # Progressive chain
                for i in range(1, len(temp_clips)):
                    inv = f"[{i}:v]"
                    # offset = previous accumulated duration - transition duration
                    offset = max(0.0, acc_dur - td)
                    v_label = f"[v{i}]"
                    filter_lines.append(f"{out_v}{inv} xfade=transition=fade:duration={td}:offset={offset} {v_label}")
                    out_v = v_label
                    if has_audio_all:
                        ina = f"[{i}:a]"
                        a_label = f"[a{i}]"
                        filter_lines.append(f"{out_a}{ina} acrossfade=d={td}:c1=tri:c2=tri {a_label}")
                        out_a = a_label
                    acc_dur = acc_dur + durations_sec[i] - td

                filter_complex = ";".join(filter_lines)
                # Output mapping with re-encode
                settings = self.QUALITY_SETTINGS.get(quality, self.QUALITY_SETTINGS[self.QUALITY_HIGH])
                cmd.extend([
                    "-filter_complex", filter_complex,
                    "-map", out_v,
                ])
                if has_audio_all and out_a:
                    cmd.extend(["-map", out_a, "-c:a", "aac", "-b:a", settings["bitrate_audio"]])
                else:
                    cmd.extend(["-an"])  # no audio
                cmd.extend([
                    "-c:v", "libx264",
                    "-crf", settings["crf"],
                    "-preset", settings["preset"],
                    "-y", output_path
                ])

                print(f"[FFmpeg] XFade command: {' '.join(cmd)}", flush=True)

                # Parse concat stage progress 60→100
                acc_total = max(0.01, sum(durations_sec) - td * (len(durations_sec) - 1))

                def _parse_ff_time(s: str) -> float:
                    import re
                    m = re.search(r"time=(\d+):(\d+):(\d+\.?\d*)", s)
                    if not m:
                        return -1.0
                    hh = int(m.group(1)); mm = int(m.group(2)); ss = float(m.group(3))
                    return hh * 3600.0 + mm * 60.0 + ss

                self.process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
                for line in self.process.stderr:
                    if self.is_cancelled:
                        self.process.terminate()
                        self.process_completed.emit(False, "Cancelled by user")
                        return
                    try:
                        print(f"[FFmpeg][Concat][stderr] {line.strip()}", flush=True)
                    except Exception:
                        pass
                    if "time=" in line:
                        cur = _parse_ff_time(line)
                        if cur >= 0:
                            pct = 60 + int(min(cur / acc_total, 1.0) * 39)
                            self.progress_updated.emit(min(pct, 99))
                self.process.wait()
                result_code = self.process.returncode

            # Cleanup temp files
            for clip in temp_clips:
                if os.path.exists(clip):
                    os.remove(clip)
            if os.path.exists(concat_file):
                os.remove(concat_file)
            try:
                os.rmdir(temp_dir)
            except Exception:
                pass

            if result_code == 0 and os.path.exists(output_path):
                self.progress_updated.emit(100)
                self.process_completed.emit(True, output_path)
            else:
                error_msg = "Concatenation failed"
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
