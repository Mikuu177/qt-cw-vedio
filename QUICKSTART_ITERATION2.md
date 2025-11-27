# 快速启动指南 - Iteration 2

## 立即运行应用

### 1. 安装依赖（如果还没有）

```bash
cd qt-cw-vedio
pip install -r requirements.txt
```

### 2. 运行 Iteration 2 版本

```bash
python src/main_v2.py
```

### 3. 可选：安装 FFmpeg（用于导出功能）

**Windows**:
1. 下载 FFmpeg: https://ffmpeg.org/download.html
2. 解压到 `C:\ffmpeg`
3. 添加到环境变量 PATH: `C:\ffmpeg\bin`
4. 重启终端，验证: `ffmpeg -version`

---

## 主要功能速览

### ✨ 新增功能（Iteration 2）

1. **视频裁剪** ✂️
   - 按 **I** 键设置入点
   - 按 **O** 键设置出点
   - 菜单 > File > Export 导出裁剪后的视频

2. **多片段时间轴** 📽️
   - 点击底部 **"+ Add Clip"** 按钮添加视频
   - 右键点击片段删除
   - 拖动重新排序

3. **标记系统** 📍
   - 按 **M** 键在当前位置添加标记
   - 按 **[** 跳到上一个标记
   - 按 **]** 跳到下一个标记

4. **高对比度模式** 🎨
   - 按 **Ctrl+Shift+H** 切换
   - 或菜单 > View > High Contrast Mode
   - 黄色文字/黑色背景，符合 WCAG AAA 标准

5. **撤销/重做** ↩️
   - **Ctrl+Z** 撤销
   - **Ctrl+Y** 重做
   - 支持所有编辑操作

6. **视频导出** 💾
   - **Ctrl+E** 打开导出对话框
   - 选择质量：高/中/低
   - 需要安装 FFmpeg

---

## 完整键盘快捷键

| 功能 | 快捷键 |
|------|--------|
| **文件** | |
| 打开视频 | Ctrl+O |
| 导出视频 | Ctrl+E |
| 退出 | Ctrl+Q |
| **编辑** | |
| 撤销 | Ctrl+Z |
| 重做 | Ctrl+Y |
| 裁剪模式 | Ctrl+T |
| 设置入点 | I |
| 设置出点 | O |
| **播放** | |
| 播放/暂停 | Space |
| 后退 5 秒 | ← |
| 前进 5 秒 | → |
| 音量增加 | ↑ |
| 音量减少 | ↓ |
| 静音 | M |
| **标记** | |
| 添加标记 | M |
| 上一个标记 | [ |
| 下一个标记 | ] |
| **视图** | |
| 全屏 | F |
| 退出全屏 | Esc |
| 高对比度 | Ctrl+Shift+H |

---

## 三个主要使用场景

### 场景 1：裁剪视频（移除不需要的部分）

1. 打开视频文件（Ctrl+O）
2. 播放到不需要的部分开始处
3. 按 **I** 键（设置入点）
4. 播放到不需要的部分结束处
5. 按 **O** 键（设置出点）
6. Ctrl+E 导出
7. 选择输出路径和质量
8. 点击 Export

**效果**: 导出的视频将跳过 In-Out 之间的部分

### 场景 2：合并多个视频片段

1. 点击底部 **"+ Add Clip"** 按钮
2. 选择第一个视频文件
3. 再次点击 **"+ Add Clip"**
4. 选择第二个视频文件
5. 重复添加所有片段
6. （可选）拖动片段重新排序
7. Ctrl+E 导出合并后的视频

**效果**: 所有片段按顺序合并成一个视频

### 场景 3：标记重要时刻

1. 打开长视频
2. 播放到重要时刻
3. 按 **M** 键添加标记
4. 继续播放，在其他重要时刻重复步骤 3
5. 使用 **[** 和 **]** 键在标记间快速跳转

**效果**: 快速导航到视频中的关键点

---

## 项目文件结构

```
qt-cw-vedio/
├── src/
│   ├── main_v2.py              # ← 启动这个文件（Iteration 2）
│   ├── ui/
│   │   ├── main_window_v2.py   # 主窗口（包含所有新功能）
│   │   ├── timeline_widget.py  # 时间轴组件
│   │   └── export_dialog.py    # 导出对话框
│   ├── video/
│   │   ├── ffmpeg_processor.py # FFmpeg 处理
│   │   ├── timeline.py         # 时间轴数据模型
│   │   └── marker.py           # 标记系统
│   └── utils/
│       ├── theme_manager.py    # 主题管理（高对比度）
│       └── command_stack.py    # 撤销/重做
├── docs/
│   ├── iteration2/
│   │   ├── README_ITERATION2.md              # 完整用户手册
│   │   ├── TESTING_CHECKLIST_ITERATION2.md   # 测试清单
│   │   ├── cognitive_walkthrough_guide.md    # 评估指南
│   │   └── iteration2_plan.md                # 开发计划
└── videos/                     # 测试视频（如果有）
```

---

## 测试建议

### 基础功能测试（5 分钟）

1. ✅ 打开视频能否正常播放
2. ✅ 播放/暂停/停止是否工作
3. ✅ 时间轴拖动是否准确
4. ✅ 音量控制是否有效
5. ✅ 全屏模式是否正常

### Iteration 2 功能测试（10 分钟）

1. ✅ 按 I 和 O 设置裁剪点，标签是否显示
2. ✅ 添加 2-3 个片段到时间轴，是否显示正确
3. ✅ 按 M 添加标记，按 [ 和 ] 导航
4. ✅ Ctrl+Shift+H 切换高对比度模式
5. ✅ 添加片段后按 Ctrl+Z 撤销，是否移除
6. ✅ Ctrl+E 打开导出对话框（不需要实际导出）

### 已知问题

- **无音频播放**: OpenCV 后端不支持音频（正常现象）
- **时间轴播放**: 只能播放单个视频，多片段播放未实现（UI 已完成）
- **需要 FFmpeg**: 导出功能需要手动安装 FFmpeg

---

## 下一步

### 完成 Iteration 2 评估
1. 招募 3-5 名测试者
2. 按照 `docs/iteration2/cognitive_walkthrough_guide.md` 进行评估
3. 记录问题和反馈
4. 撰写评估报告

### 准备 Iteration 3
基于评估反馈，计划改进：
- 国际化（中英文切换）
- 时间轴播放功能
- 性能优化
- SUS 问卷评估

---

## 帮助与支持

### 常见问题

**Q: 视频无法加载？**
A: 检查视频编码格式，推荐 H.264 MP4

**Q: 导出按钮点击后无反应？**
A: 确认已安装 FFmpeg 并添加到 PATH

**Q: 高对比度模式下文字看不清？**
A: 调整显示器亮度，黄色/黑色应该是 19:1 对比度

**Q: 时间轴片段无法添加？**
A: 检查控制台错误信息，确认文件路径正确

### 文档位置

- **完整手册**: `docs/iteration2/README_ITERATION2.md`
- **测试清单**: `docs/iteration2/TESTING_CHECKLIST_ITERATION2.md`
- **开发文档**: `CLAUDE.md`

---

**祝使用愉快！**

如有问题，请查看详细文档或报告 GitHub Issues。
