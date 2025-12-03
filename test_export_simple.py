#!/usr/bin/env python3
"""
简单的导出测试 - 模拟导出流程

这个脚本模拟用户点击导出按钮后的完整流程
"""

import os
import sys
import tempfile

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from video.ffmpeg_processor import FFmpegProcessor
from video.timeline import Timeline

def test_export_timeline():
    """测试导出时间轴"""
    
    print("[TEST] 创建时间轴...")
    timeline = Timeline()
    
    # 获取视频文件
    video_dir = os.path.join(os.path.dirname(__file__), 'videos')
    video_files = [f for f in os.listdir(video_dir) if f.endswith(('.mp4', '.avi', '.mov', '.mkv'))]
    
    print(f"[TEST] 找到 {len(video_files)} 个视频文件")
    
    if len(video_files) < 2:
        print("[ERROR] 需要至少 2 个视频文件")
        return False
    
    # 添加片段到时间轴
    print("[TEST] 添加片段到时间轴...")
    
    # 导入 OpenCV 来获取视频时长
    import cv2
    
    for i, video_file in enumerate(video_files[:2]):
        video_path = os.path.join(video_dir, video_file)
        
        # 获取视频时长
        cap = cv2.VideoCapture(video_path)
        if cap.isOpened():
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration_ms = int((frame_count / fps) * 1000) if fps > 0 else 10000
            cap.release()
        else:
            duration_ms = 10000
        
        clip = timeline.add_clip(video_path, duration_ms=duration_ms)
        print(f"  片段 {i+1}: {video_file} (ID: {clip.id}, 时长: {duration_ms}ms)")
    
    # 获取排序后的片段
    clips = timeline.get_sorted_clips()
    print(f"\n[TEST] 时间轴中有 {len(clips)} 个片段")
    print(f"[TEST] 总时长: {timeline.get_total_duration()}ms")
    
    # 准备导出
    output_dir = os.path.join(video_dir, 'exports')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'test_export_simple.mp4')
    
    print(f"\n[TEST] 准备导出...")
    print(f"  输出文件: {output_file}")
    print(f"  质量: high")
    print(f"  过渡: 禁用")
    
    # 创建处理器
    processor = FFmpegProcessor()
    
    # 准备片段数据
    clip_data = [
        (clip.source_path, clip.start_time_ms, clip.end_time_ms)
        for clip in clips
    ]
    
    print(f"\n[TEST] 片段数据:")
    for i, (path, start, end) in enumerate(clip_data):
        print(f"  {i+1}. {os.path.basename(path)} ({start}ms - {end}ms)")
    
    # 连接信号
    progress_values = []
    
    def on_progress(pct):
        progress_values.append(pct)
        print(f"[PROGRESS] {pct}%")
    
    def on_completed(success, msg):
        if success:
            print(f"[SUCCESS] 导出完成: {msg}")
        else:
            print(f"[ERROR] 导出失败: {msg}")
    
    processor.progress_updated.connect(on_progress)
    processor.process_completed.connect(on_completed)
    
    # 执行导出
    print(f"\n[TEST] 开始导出...")
    print("=" * 60)
    
    processor.concatenate_clips(
        clip_data,
        output_file,
        quality="high",
        transitions_enabled=False,
        transition_ms=500
    )
    
    print("=" * 60)
    
    # 检查结果
    if os.path.exists(output_file):
        file_size = os.path.getsize(output_file)
        print(f"\n[SUCCESS] 导出成功")
        print(f"  文件大小: {file_size / 1024 / 1024:.2f} MB")
        print(f"  进度值: {progress_values}")
        return True
    else:
        print(f"\n[ERROR] 导出失败 - 文件未创建")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("简单导出测试")
    print("=" * 60)
    
    success = test_export_timeline()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ 测试成功")
        sys.exit(0)
    else:
        print("❌ 测试失败")
        sys.exit(1)

