# Bug Fix: Timeline Add Clip FFprobe Error

**日期**: 2025-11-26
**问题**: 点击 "Add Clip" 时出现 `[FFprobe] Error getting video info: [WinError 2] 系统找不到指定的文件。`
**状态**: ✅ **已修复**

---

## 问题描述

### 错误日志
```
[FFprobe] Error getting video info: [WinError 2] 系统找不到指定的文件。
[Timeline] Added clip: TimelineClip(id=1, source='...mp4', start=0ms, duration=10000ms, position=0ms)
```

### 症状
- 点击 "+ Add Clip" 按钮添加视频片段
- 控制台显示 FFprobe 错误
- 片段被添加，但时长显示为 **10000ms**（10秒）而不是实际时长 **151699ms**

### 根本原因
1. `timeline_widget.py` 调用 `get_video_info()` 使用 **ffprobe** 获取视频信息
2. 用户**没有安装 FFmpeg**，所以 ffprobe 命令不存在
3. 代码回退到占位符时长（10秒），导致时长不准确

---

## 修复方案

### 实现的改进

**修改文件**: `src/ui/timeline_widget.py`

**新增方法**: `get_video_duration()` - 三层回退机制

```python
def get_video_duration(self, file_path):
    """
    Get video duration using multiple fallback methods.

    Try in order:
    1. FFprobe (most accurate, requires FFmpeg) ← 最准确，但需要 FFmpeg
    2. OpenCV (works without FFmpeg)           ← 备选，已安装
    3. Placeholder (10 seconds)                ← 最后的保底
    """
```

### 工作流程

```
点击 Add Clip
    ↓
选择视频文件
    ↓
获取视频时长
    ├─→ 尝试 FFprobe ──→ ✗ 失败（未安装 FFmpeg）
    ├─→ 尝试 OpenCV  ──→ ✓ 成功（151699ms）
    └─→ 占位符 10s   ──→ （不会执行）
    ↓
使用正确时长添加片段到时间轴
```

---

## 测试验证

### 测试脚本
创建了 `test_duration.py` 来验证两种方法：

```bash
python test_duration.py
```

### 测试结果
```
Testing OpenCV method:
------------------------------------------------------------
FPS: 30.00
Frame count: 4551
Duration: 151699ms (151.70 seconds)  ✓ 成功
Duration (formatted): 2m 31s

Testing FFprobe method:
------------------------------------------------------------
[FFprobe] Error getting video info: [WinError 2] 系统找不到指定的文件。
ERROR: get_video_info returned None   ✗ 失败（预期）

COMPARISON:
------------------------------------------------------------
OpenCV:  151699ms [OK]               ✓ 可用
FFprobe: FAILED (FFmpeg not installed) ✗ 不可用（但不影响功能）
```

---

## 修复效果

### 修复前 ❌
```
[FFprobe] Error getting video info: [WinError 2] ...
[Timeline] Added clip: duration=10000ms  ← 错误的时长
```

**问题**：
- 片段时长不准确（10秒 vs 实际 151秒）
- 时间轴统计信息错误
- 导出的视频时长会不对

### 修复后 ✅
```
[Timeline] FFprobe unavailable: ...
[Timeline] Got duration from OpenCV: 151699ms (4551 frames at 30.00 fps)
[Timeline] Added clip: duration=151699ms  ← 正确的时长
```

**改进**：
- ✅ 准确的视频时长
- ✅ 无需安装 FFmpeg 也能正常工作
- ✅ 自动回退机制，更加健壮
- ✅ 详细的日志输出，便于调试

---

## 用户操作指南

### 现在你可以：

1. **添加片段到时间轴**（无需 FFmpeg）
   ```
   点击 "+ Add Clip"
   选择视频文件
   ✓ 片段会以正确的时长添加
   ```

2. **查看准确的时间轴信息**
   ```
   底部显示："3 clip(s) | Total duration: 455.1s"  ← 准确
   而不是："3 clip(s) | Total duration: 30.0s"    ← 之前错误
   ```

3. **导出多片段视频**（需要 FFmpeg）
   ```
   添加片段 → Ctrl+E 导出
   如果没有 FFmpeg，会提示安装
   ```

---

## 何时需要 FFmpeg？

### 不需要 FFmpeg ✅
- ✅ 播放视频
- ✅ 添加片段到时间轴（使用 OpenCV 获取时长）
- ✅ 删除/重排片段
- ✅ 添加标记
- ✅ 撤销/重做
- ✅ 高对比度模式

### 需要 FFmpeg ❌
- ❌ **导出视频**（裁剪/合并）
- ❌ **获取视频元数据**（编码格式、分辨率等详细信息）

### 安装 FFmpeg（可选）

如果你想使用导出功能：

1. **下载**: https://ffmpeg.org/download.html
2. **解压**: 到 `C:\ffmpeg`
3. **添加到 PATH**:
   - 右键"此电脑" → 属性 → 高级系统设置
   - 环境变量 → Path → 新建 → `C:\ffmpeg\bin`
4. **验证**:
   ```bash
   ffmpeg -version
   ```

---

## 技术细节

### OpenCV 获取时长原理

```python
cap = cv2.VideoCapture(file_path)
fps = cap.get(cv2.CAP_PROP_FPS)           # 帧率: 30.00
frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # 总帧数: 4551

duration_ms = (frame_count / fps) * 1000  # 4551 / 30 * 1000 = 151700ms
```

### 为什么 OpenCV 足够准确？

- ✅ 直接读取视频容器元数据
- ✅ 不需要解码整个视频
- ✅ 准确度与 FFprobe 相差 < 100ms
- ✅ 对于时间轴显示来说完全足够

### FFprobe vs OpenCV 对比

| 特性 | FFprobe | OpenCV |
|------|---------|--------|
| 准确度 | ⭐⭐⭐⭐⭐ 最高 | ⭐⭐⭐⭐ 很高 |
| 依赖 | 需要 FFmpeg | 仅需 cv2 |
| 信息量 | 完整元数据 | 基本信息 |
| 速度 | 快 | 非常快 |
| 用于时间轴 | ✓ 完美 | ✓ 足够 |

---

## 相关文件

### 修改的文件
- `src/ui/timeline_widget.py` - 添加 `get_video_duration()` 方法

### 新增的文件
- `test_duration.py` - 测试脚本（验证修复）
- `BUGFIX_TIMELINE.md` - 本文档

### 相关文档
- `HOW_TO_RUN.md` - 完整运行指南
- `FINAL_STATUS.md` - 项目状态

---

## 下次运行应用

```bash
python src/main_v2.py
```

### 预期日志（正常）

```
[Theme] Applied normal theme
[DEBUG] OpenCVVideoPlayer initialized
[DEBUG] Loading video with OpenCV: ...
[DEBUG] Video loaded: Total frames: 4551, FPS: 30.00, Duration: 151699 ms

# 点击 Add Clip 后
[Timeline] FFprobe unavailable: [WinError 2] 系统找不到指定的文件。  ← 预期的
[Timeline] Got duration from OpenCV: 151699ms (4551 frames at 30.00 fps)  ← 成功
[Timeline] Added clip: TimelineClip(..., duration=151699ms, ...)  ← 正确
```

### 关键指标

- ✅ 没有"系统找不到指定的文件"错误在关键路径
- ✅ 显示"Got duration from OpenCV"表示回退成功
- ✅ 片段时长准确（151699ms 而不是 10000ms）

---

## 总结

### 问题
用户没有安装 FFmpeg，导致添加片段时时长不准确（10秒占位符）

### 解决方案
添加 OpenCV 作为备选方案，三层回退机制：FFprobe → OpenCV → Placeholder

### 结果
- ✅ 无需 FFmpeg 也能正常使用时间轴功能
- ✅ 视频时长准确
- ✅ 代码更加健壮
- ✅ 用户体验改善

### 影响范围
- 仅影响 `timeline_widget.py` 一个文件
- 向后兼容（有 FFmpeg 的用户依然优先使用 FFprobe）
- 无破坏性更改

---

**修复完成！现在可以正常使用 Add Clip 功能了。** ✅

*Bug Fix Date: 2025-11-26*
*Fixed By: Claude Code*
*Tested: ✓ Verified with test_duration.py*
