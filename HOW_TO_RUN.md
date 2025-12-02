# 如何运行视频编辑器 - 完整指南

## 📋 前置要求

### 必需（Required）
1. **Python 3.8 或更高版本**
   ```bash
   python --version
   # 应该显示 Python 3.8.x 或更高
   ```

2. **安装依赖包**
   ```bash
   cd qt-cw-vedio
   pip install -r requirements.txt
   ```

   依赖包括：
   - PyQt5==5.15.10
   - opencv-python>=4.8.0

### 可选（Optional，但推荐）
3. **FFmpeg**（用于视频导出功能）

   **Windows 安装步骤**：
   1. 下载：https://ffmpeg.org/download.html
   2. 选择 "Windows builds from gyan.dev"
   3. 下载 "ffmpeg-release-full.7z"
   4. 解压到 `C:\ffmpeg`
   5. 添加到环境变量 PATH：
      - 右键"此电脑" → "属性"
      - "高级系统设置" → "环境变量"
      - 在"系统变量"中找到 `Path`，点击"编辑"
      - 点击"新建"，输入 `C:\ffmpeg\bin`
      - 点击"确定"保存
   6. 重启命令行，验证安装：
      ```bash
      ffmpeg -version
      ```

---

## 🚀 启动应用

### 方法 1：使用命令行（推荐）

```bash
# 1. 进入项目目录
cd "C:\Users\Administrator\Desktop\代谢\用户界面QT-傲宇\qt-cw-vedio"

# 2. 运行 Iteration 2 版本
python src/main_v2.py
```

### 方法 2：使用 Python IDLE
1. 打开 `src/main_v2.py`
2. 按 F5 运行

### 方法 3：双击运行（需要配置）
1. 创建批处理文件 `run.bat`：
   ```batch
   @echo off
   cd /d "%~dp0"
   python src/main_v2.py
   pause
   ```
2. 双击 `run.bat`

---

## ✅ 验证安装

启动后应该看到：
- ✅ 窗口标题：`Video Editor/Player - XJCO2811 (Iteration 2)`
- ✅ 菜单栏：File, Edit, View, Markers, Help
- ✅ 播放控件在中间
- ✅ 底部有时间轴区域（Timeline）
- ✅ 如果 `videos/` 文件夹中有视频，会自动加载

### 常见启动问题

#### 问题 1：`ModuleNotFoundError: No module named 'PyQt5'`
**解决方案**：
```bash
pip install PyQt5==5.15.10
```

#### 问题 2：`ModuleNotFoundError: No module named 'cv2'`
**解决方案**：
```bash
pip install opencv-python
```

#### 问题 3：窗口打开后立即关闭
**解决方案**：
- 检查控制台是否有错误信息
- 尝试在命令行中运行，查看错误详情

#### 问题 4：`ImportError: DLL load failed`
**解决方案**：
- 更新 Visual C++ Redistributable：https://aka.ms/vs/17/release/vc_redist.x64.exe

---

## 🎬 快速上手（5 分钟）

### 1. 打开视频
- **方法 A**：菜单 > File > Open Video（Ctrl+O）
- **方法 B**：如果 `videos/` 文件夹有视频，会自动加载

### 2. 基础播放
- **播放/暂停**：按 Space 键 或 点击 ▶️ 按钮
- **拖动时间轴**：鼠标拖动滑块
- **调节音量**：使用音量滑块（注意：OpenCV 无音频播放）
- **全屏**：按 F 键

### 3. 添加标记（导航功能）
1. 播放到重要位置（比如 0:30）
2. 按 **M** 键
3. 顶部会出现彩色旗帜
4. 按 **[** 和 **]** 在标记间跳转

### 4. 添加多个片段到时间轴
1. 滚动到窗口底部，找到 "Timeline" 区域
2. 点击 **"+ Add Clip"** 按钮
3. 选择第一个视频文件
4. 重复步骤 2-3 添加更多片段
5. 查看底部统计："3 clip(s) | Total duration: XX.Xs"

### 5. 导出视频
1. 按 **Ctrl+E** 或 菜单 > File > Export Video
2. 点击 "Browse..." 选择保存位置
3. 选择质量（High/Medium/Low）
4. 点击 "Export"
5. 等待进度条完成

### 6. 查看所有快捷键
- 按 **F1** 或 菜单 > Help > Keyboard Shortcuts

---

## 🎯 核心功能详解

### 功能 1：视频裁剪（Trimming）

**用途**：移除视频中不需要的部分

**步骤**：
1. 打开视频
2. 播放到你想保留的**起始位置**
3. 按 **I** 键（入点，绿色显示）
4. 播放到你想保留的**结束位置**
5. 按 **O** 键（出点，红色显示）
6. Ctrl+E 导出
7. 导出的视频只包含 In-Out 之间的内容

**示例**：移除前 15 秒
- 播放到 0:15 → 按 I
- 播放到视频结尾 → 按 O
- 导出

### 功能 2：多片段合并（Multi-Clip Timeline）

**用途**：把多个视频合并成一个

**步骤**：
1. 点击底部 **"+ Add Clip"**
2. 选择 intro.mp4
3. 再点 **"+ Add Clip"**
4. 选择 main.mp4
5. 再点 **"+ Add Clip"**
6. 选择 outro.mp4
7. Ctrl+E 导出

**结果**：3 个视频按顺序合并

### 功能 3：标记系统（Markers）

**用途**：快速导航长视频

**步骤**：
1. 播放到重要时刻
2. 按 **M** 添加标记
3. 重复步骤 1-2 添加更多标记
4. 使用 **[** 和 **]** 在标记间跳转
5. 或直接点击顶部的彩色旗帜

**颜色**：自动循环（红→蓝→绿→黄→橙→紫→青→粉）

### 功能 4：高对比度模式（Accessibility）

**用途**：为视力受损用户提供更清晰的界面

**启用**：
- Ctrl+Shift+H 或
- View > High Contrast Mode

**效果**：
- 黑色背景
- 黄色文字
- 加粗边框
- 19:1 对比度（WCAG AAA）

### 功能 5：撤销/重做

**支持的操作**：
- 添加/删除片段
- 添加/删除标记
- 重排片段

**使用**：
- **Ctrl+Z** 撤销
- **Ctrl+Y** 重做

---

## ⌨️ 完整键盘快捷键表

### 文件操作
| 快捷键 | 功能 |
|--------|------|
| Ctrl+O | 打开视频 |
| Ctrl+E | 导出视频 |
| Ctrl+Q | 退出程序 |

### 编辑操作
| 快捷键 | 功能 |
|--------|------|
| Ctrl+Z | 撤销 |
| Ctrl+Y | 重做 |
| Ctrl+T | 裁剪模式 |
| I | 设置入点 |
| O | 设置出点 |

### 播放控制
| 快捷键 | 功能 |
|--------|------|
| Space | 播放/暂停 |
| ← | 后退 5 秒 |
| → | 前进 5 秒 |
| ↑ | 音量增加 |
| ↓ | 音量减少 |
| M | 静音 |

### 标记导航
| 快捷键 | 功能 |
|--------|------|
| M | 添加标记 |
| [ | 上一个标记 |
| ] | 下一个标记 |

### 视图控制
| 快捷键 | 功能 |
|--------|------|
| F | 全屏 |
| Esc | 退出全屏 |
| Ctrl+Shift+H | 高对比度 |

### 帮助
| 快捷键 | 功能 |
|--------|------|
| F1 | 快捷键帮助 |

---

## 🎥 准备测试视频

### 选项 1：使用自己的视频
1. 创建 `videos/` 文件夹（如果不存在）
2. 复制你的 MP4 视频文件到这个文件夹
3. 重启应用，会自动加载第一个视频

### 选项 2：下载示例视频
1. 从以下网站下载免费视频：
   - Pexels: https://www.pexels.com/videos/
   - Pixabay: https://www.pixabay.com/videos/
2. 保存到 `videos/` 文件夹

### 推荐的测试视频
- **短片段**（5-10 秒）：用于测试多片段合并
- **长视频**（3-5 分钟）：用于测试标记和裁剪
- **格式**：MP4 (H.264) 最佳兼容性

---

## ⚠️ 已知限制

### 1. OpenCV 无音频播放
- **现象**：播放视频时听不到声音
- **原因**：OpenCV 后端不支持音频
- **影响**：仅播放时无声，导出的视频包含音频
- **解决方案**：这是设计选择，不影响核心功能

### 2. 时间轴播放未实现
- **现象**：添加多个片段到时间轴后，不能直接预览合并效果
- **解决方案**：需要导出后在 VLC 等播放器中查看

### 3. FFmpeg 需手动安装
- **现象**：点击导出时提示 "FFmpeg Not Found"
- **解决方案**：按照上面的 FFmpeg 安装步骤操作

### 4. 大视频文件性能
- **现象**：导出大视频（>500MB）时可能较慢
- **原因**：FFmpeg 编码是 CPU 密集型
- **解决方案**：选择 Medium 或 Low 质量加快速度

---

## 🐛 故障排除

### 问题：视频无法加载
**可能原因**：
1. 视频编码格式不支持
2. 文件路径包含中文或特殊字符

**解决方案**：
1. 确保使用 H.264 编码的 MP4 文件
2. 将文件移动到无中文的路径

### 问题：导出功能无响应
**检查步骤**：
1. 确认已安装 FFmpeg：`ffmpeg -version`
2. 确认已添加到 PATH
3. 重启应用
4. 查看控制台错误信息

### 问题：高对比度模式文字看不清
**解决方案**：
1. 调整显示器亮度
2. 确保显示器对比度设置正确
3. 黄色/黑色应该是 19:1 对比度

### 问题：快捷键不工作
**检查**：
1. 确保窗口处于焦点状态
2. 按 F1 查看完整快捷键列表
3. 某些快捷键（如 M）在不同上下文有不同含义

---

## 📚 更多资源

### 文档位置
- **完整用户手册**：`docs/iteration2/README_ITERATION2.md`
- **测试清单**：`docs/iteration2/TESTING_CHECKLIST_ITERATION2.md`
- **认知走查指南**：`docs/iteration2/cognitive_walkthrough_guide.md`
- **开发文档**：`CLAUDE.md`

### 在线帮助
- **GitHub 仓库**：https://github.com/Mikuu177/qt-cw-vedio
- **FFmpeg 官网**：https://ffmpeg.org
- **PyQt5 文档**：https://www.riverbankcomputing.com/static/Docs/PyQt5/

---

## 🎓 用于评估

### Iteration 2 认知走查任务

**任务 1：裁剪视频**
- 打开视频
- 设置 In/Out 点
- 导出裁剪后的视频

**任务 2：合并片段**
- 添加 3 个片段到时间轴
- 重新排序
- 导出合并视频

**任务 3：使用标记**
- 添加 3 个标记
- 使用 [ 和 ] 导航
- 验证跳转正确

### 评估指标
- 任务完成率（目标：>80%）
- 任务时间（分钟）
- 错误次数
- 用户满意度（1-5 分）

---

## 📞 获取帮助

### 应用内帮助
- 按 **F1** 查看快捷键
- Help > About 查看版本信息

### 技术支持
- 查看 `docs/` 文件夹中的详细文档
- 检查控制台错误信息
- 报告 GitHub Issues

---

**祝使用愉快！如果遇到问题，请先查看"故障排除"部分。**

*最后更新：2025-11-26*
*版本：Iteration 2 Final*
