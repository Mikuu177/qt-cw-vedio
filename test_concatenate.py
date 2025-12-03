#!/usr/bin/env python3
"""
测试视频合成功能 - 直接测试 FFmpeg 合成

这个脚本测试两个视频文件的合成功能，不依赖 UI
"""

import os
import sys
import subprocess

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from video.ffmpeg_processor import FFmpegProcessor

def test_concatenate():
    """测试视频合成"""
    
    # 获取视频文件夹中的视频
    video_dir = os.path.join(os.path.dirname(__file__), 'videos')
    
    # 列出所有视频文件
    video_files = [f for f in os.listdir(video_dir) if f.endswith(('.mp4', '.avi', '.mov', '.mkv'))]
    print(f"[TEST] 找到 {len(video_files)} 个视频文件:")
    for i, f in enumerate(video_files):
        print(f"  {i+1}. {f}")
    
    if len(video_files) < 2:
        print("[ERROR] 需要至少 2 个视频文件来测试合成")
        return False
    
    # 选择前两个视频
    video1 = os.path.join(video_dir, video_files[0])
    video2 = os.path.join(video_dir, video_files[1])
    
    print(f"\n[TEST] 选择的视频:")
    print(f"  视频 1: {video_files[0]}")
    print(f"  视频 2: {video_files[1]}")
    
    # 输出文件
    output_file = os.path.join(video_dir, 'exports', 'test_concatenate.mp4')
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    print(f"\n[TEST] 输出文件: {output_file}")
    
    # 检查 FFmpeg
    print(f"\n[TEST] 检查 FFmpeg 可用性...")
    if not FFmpegProcessor.check_ffmpeg_available():
        print("[ERROR] FFmpeg 未安装或不在 PATH 中")
        print("[INFO] 请安装 FFmpeg: https://ffmpeg.org/download.html")
        return False
    print("[OK] FFmpeg 已安装")
    
    # 创建处理器
    print(f"\n[TEST] 创建 FFmpeg 处理器...")
    processor = FFmpegProcessor()
    
    # 准备片段数据
    # 格式: (source_path, start_ms, end_ms)
    # 使用整个视频，所以 start=0, end=很大的数字
    clips = [
        (video1, 0, 999999999),  # 使用整个视频 1
        (video2, 0, 999999999),  # 使用整个视频 2
    ]
    
    print(f"[TEST] 片段数据:")
    for i, (path, start, end) in enumerate(clips):
        print(f"  片段 {i+1}: {os.path.basename(path)} ({start}ms - {end}ms)")
    
    # 连接信号
    def on_progress(pct):
        print(f"[PROGRESS] {pct}%")
    
    def on_completed(success, msg):
        if success:
            print(f"[SUCCESS] 合成完成: {msg}")
        else:
            print(f"[ERROR] 合成失败: {msg}")
    
    processor.progress_updated.connect(on_progress)
    processor.process_completed.connect(on_completed)
    
    # 执行合成
    print(f"\n[TEST] 开始合成...")
    print("=" * 60)
    
    processor.concatenate_clips(
        clips,
        output_file,
        quality="high",
        transitions_enabled=False,
        transition_ms=500
    )
    
    print("=" * 60)
    
    # 检查输出文件
    if os.path.exists(output_file):
        file_size = os.path.getsize(output_file)
        print(f"\n[SUCCESS] 输出文件已创建")
        print(f"  文件大小: {file_size / 1024 / 1024:.2f} MB")
        
        # 验证视频
        print(f"\n[TEST] 验证输出视频...")
        try:
            result = subprocess.run([
                'ffprobe', '-v', 'error',
                '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1:noprint_wrappers=1',
                output_file
            ], capture_output=True, timeout=10)
            
            if result.returncode == 0:
                duration = float(result.stdout.decode().strip())
                print(f"  视频时长: {duration:.2f} 秒")
                print(f"[OK] 输出视频有效")
                return True
            else:
                print(f"[ERROR] 无法验证视频")
                return False
        except Exception as e:
            print(f"[ERROR] 验证失败: {e}")
            return False
    else:
        print(f"\n[ERROR] 输出文件未创建")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("视频合成功能测试")
    print("=" * 60)
    
    success = test_concatenate()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ 测试成功")
        sys.exit(0)
    else:
        print("❌ 测试失败")
        sys.exit(1)


