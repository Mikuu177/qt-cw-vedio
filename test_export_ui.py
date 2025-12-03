#!/usr/bin/env python3
"""
测试导出 UI 流程

这个脚本测试完整的导出流程，包括对话框和实际导出
"""

import os
import sys
import time

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTimer

from ui.main_window_v2 import MainWindow

def test_export_ui():
    """测试导出 UI"""
    
    print("[TEST] 启动应用...")
    app = QApplication(sys.argv)
    
    # 创建主窗口
    window = MainWindow(app)
    window.show()
    
    print("[TEST] 应用已启动")
    print("[TEST] 等待 2 秒...")
    
    # 延迟后触发导出
    def trigger_export():
        print("[TEST] 触发导出...")
        
        # 检查是否有片段
        clips = window.timeline.get_sorted_clips()
        print(f"[TEST] 时间轴中有 {len(clips)} 个片段")
        
        if len(clips) > 0:
            print("[TEST] 触发 Ctrl+E (导出)...")
            window.export_video()
        else:
            print("[TEST] 没有片段，无法导出")
            print("[TEST] 添加一个片段...")
            
            # 添加一个片段
            video_dir = os.path.join(os.path.dirname(__file__), 'videos')
            video_files = [f for f in os.listdir(video_dir) if f.endswith(('.mp4', '.avi', '.mov', '.mkv'))]
            
            if len(video_files) > 0:
                video_path = os.path.join(video_dir, video_files[0])
                print(f"[TEST] 添加视频: {video_files[0]}")
                
                clip = window.timeline.add_clip(video_path)
                print(f"[TEST] 片段已添加: {clip.id}")
                
                # 再次触发导出
                print("[TEST] 再次触发导出...")
                window.export_video()
    
    # 使用 QTimer 延迟执行
    timer = QTimer()
    timer.setSingleShot(True)
    timer.timeout.connect(trigger_export)
    timer.start(2000)  # 2 秒后执行
    
    # 运行应用
    print("[TEST] 运行应用事件循环...")
    sys.exit(app.exec_())

if __name__ == '__main__':
    print("=" * 60)
    print("导出 UI 测试")
    print("=" * 60)
    
    test_export_ui()


