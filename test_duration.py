"""
Test video duration detection methods.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_opencv_duration(video_path):
    """Test getting duration using OpenCV."""
    print(f"\nTesting OpenCV method on: {video_path}")
    print("-" * 60)

    try:
        import cv2
        cap = cv2.VideoCapture(video_path)

        if cap.isOpened():
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            print(f"FPS: {fps:.2f}")
            print(f"Frame count: {frame_count}")

            if fps > 0 and frame_count > 0:
                duration_ms = int((frame_count / fps) * 1000)
                duration_sec = duration_ms / 1000.0
                print(f"Duration: {duration_ms}ms ({duration_sec:.2f} seconds)")
                print(f"Duration (formatted): {int(duration_sec // 60)}m {int(duration_sec % 60)}s")
                cap.release()
                return duration_ms
            else:
                print("ERROR: Invalid FPS or frame count")
                cap.release()
        else:
            print("ERROR: Could not open video")
    except Exception as e:
        print(f"ERROR: {e}")

    return None

def test_ffprobe_duration(video_path):
    """Test getting duration using FFprobe."""
    print(f"\nTesting FFprobe method on: {video_path}")
    print("-" * 60)

    try:
        from video.ffmpeg_processor import get_video_info
        info = get_video_info(video_path)

        if info:
            print(f"Duration: {info['duration_ms']}ms")
            print(f"Resolution: {info['width']}x{info['height']}")
            print(f"FPS: {info['fps']:.2f}")
            print(f"Codec: {info['codec']}")
            return info['duration_ms']
        else:
            print("ERROR: get_video_info returned None")
    except Exception as e:
        print(f"ERROR: {e}")
        print("(This is expected if FFmpeg is not installed)")

    return None

if __name__ == "__main__":
    # Find a test video
    videos_dir = os.path.join(os.path.dirname(__file__), 'videos')

    if os.path.exists(videos_dir):
        video_files = [f for f in os.listdir(videos_dir)
                      if f.endswith(('.mp4', '.avi', '.mkv', '.mov'))]

        if video_files:
            test_video = os.path.join(videos_dir, video_files[0])
            print(f"Testing with: {test_video}")
            print("=" * 60)

            # Test both methods
            opencv_duration = test_opencv_duration(test_video)
            ffprobe_duration = test_ffprobe_duration(test_video)

            # Compare results
            print("\n" + "=" * 60)
            print("COMPARISON:")
            print("-" * 60)
            if opencv_duration:
                print(f"OpenCV:  {opencv_duration}ms [OK]")
            else:
                print("OpenCV:  FAILED [ERROR]")

            if ffprobe_duration:
                print(f"FFprobe: {ffprobe_duration}ms [OK]")
            else:
                print("FFprobe: FAILED (FFmpeg not installed)")

            if opencv_duration and ffprobe_duration:
                diff = abs(opencv_duration - ffprobe_duration)
                print(f"\nDifference: {diff}ms")
                if diff < 100:  # Less than 100ms difference is acceptable
                    print("Result: MATCH [OK]")
                else:
                    print("Result: MISMATCH (but both work)")
        else:
            print("No video files found in videos/ directory")
    else:
        print("videos/ directory not found")
