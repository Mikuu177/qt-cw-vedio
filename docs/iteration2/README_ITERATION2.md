# Video Editor/Player - Iteration 2

## What's New in Iteration 2 🎬

Iteration 2 transforms the basic video player into a full-featured video editor with advanced accessibility support.

### Major Features Added

#### 1. **Video Trimming/Cutting** ✂️
- Set In/Out points using **I** and **O** keys
- Visual indicators show trim range
- Export trimmed segments using FFmpeg

#### 2. **Multi-Clip Timeline** 📽️
- Add multiple video clips to timeline
- Drag-and-drop to reorder clips
- Visual timeline widget with clip thumbnails
- Export combined videos

#### 3. **Marker System** 📍
- Press **M** to add markers at current position
- Navigate with **[** (previous) and **]** (next) keys
- Click markers to jump to positions
- Automatic color coding

#### 4. **High Contrast Mode** 🎨
- Toggle with **Ctrl+Shift+H** or View menu
- WCAG 2.1 Level AAA compliant (7:1 contrast ratio)
- Yellow text on black background
- Bold fonts and thick borders for visibility

#### 5. **Export Functionality** 💾
- Export with quality presets (High/Medium/Low)
- Progress bar with status updates
- FFmpeg-powered encoding

#### 6. **Undo/Redo System** ↩️
- **Ctrl+Z** to undo actions
- **Ctrl+Y** to redo actions
- Supports all editing operations (add/remove clips, markers)

---

## Installation & Setup

### Prerequisites

1. **Python 3.8+**
   ```bash
   python --version
   ```

2. **Required Python Packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **FFmpeg (Optional but Recommended)**
   - Download from: https://ffmpeg.org/download.html
   - Add to system PATH
   - Verify installation:
     ```bash
     ffmpeg -version
     ```

   **Note**: FFmpeg is required for video export functionality. The application will work without it but export features will be limited.

### Quick Start

1. **Navigate to project directory**
   ```bash
   cd qt-cw-vedio
   ```

2. **Run Iteration 2 version**
   ```bash
   python src/main_v2.py
   ```

3. **Load a video**
   - File > Open Video (Ctrl+O)
   - Or the app will auto-load a sample video if available

---

## User Guide

### Basic Playback (from Iteration 1)

| Action | Keyboard Shortcut | Button |
|--------|------------------|--------|
| Play/Pause | Space | ▶️/⏸️ |
| Stop | - | ⏹️ |
| Rewind 10s | - | ⏪ |
| Fast-Forward 10s | - | ⏩ |
| Seek ±5s | Left/Right Arrow | Timeline slider |
| Volume Up/Down | Up/Down Arrow | Volume slider |
| Mute/Unmute | M | 🔊 |
| Fullscreen | F | ⛶ |
| Speed Control | - | Dropdown (0.25x-2x) |

### Video Trimming (NEW)

**Scenario**: Remove unwanted sections from a video

1. **Enable Trim Mode** (optional): Edit > Trim Mode (Ctrl+T)
2. **Set In Point**: Play to desired start position, press **I**
3. **Set Out Point**: Play to desired end position, press **O**
4. **Export**: File > Export Video (Ctrl+E)
5. **Clear Trim Points**: Edit > Clear Trim Points

**Visual Feedback**:
- In point shown in green: "In: MM:SS"
- Out point shown in red: "Out: MM:SS"

### Multi-Clip Timeline (NEW)

**Scenario**: Combine multiple videos into one

1. **Add First Clip**: Click "+ Add Clip" in timeline widget
2. **Select Video**: Choose video file from dialog
3. **Add More Clips**: Repeat steps 1-2 for additional clips
4. **Reorder (Optional)**: Drag clips left/right to reorder
5. **Delete Clip**: Right-click clip > Delete Clip
6. **Export Combined Video**: File > Export Video (Ctrl+E)

**Timeline Info**: Bottom of timeline shows "N clip(s) | Total duration: XX.Xs"

### Marker System (NEW)

**Scenario**: Navigate long videos efficiently

**Add Marker**:
1. Play to important moment
2. Press **M** key
3. Marker appears as colored flag in marker bar

**Navigate Markers**:
- Click marker to jump to position
- Press **[** for previous marker
- Press **]** for next marker

**Marker Colors**: Automatically cycle through red, blue, green, yellow, orange, purple, cyan, pink

### High Contrast Mode (NEW)

**For Visually Impaired Users**:

**Toggle On/Off**:
- Menu: View > High Contrast Mode
- Keyboard: Ctrl+Shift+H

**High Contrast Theme**:
- Black background (#000000)
- Yellow text (#FFFF00)
- White borders (3-4px thick)
- Bold fonts (11pt)
- Enhanced focus indicators (cyan border)

**WCAG Compliance**: Exceeds Level AAA (19:1 contrast ratio for yellow/black)

### Export Video (NEW)

1. **Open Export Dialog**: File > Export Video (Ctrl+E)
2. **Choose Output Path**: Click "Browse..." button
3. **Select Quality**:
   - **High**: 1080p, CRF 18 (best quality, larger file)
   - **Medium**: 720p, CRF 23 (balanced)
   - **Low**: 480p, CRF 28 (smaller file)
4. **Click Export**: Progress bar shows encoding status
5. **Wait for Completion**: Success dialog appears when done

**Note**: Requires FFmpeg installed and in system PATH

### Undo/Redo (NEW)

**Supported Actions**:
- Add/remove clips from timeline
- Add/remove markers
- Reorder clips

**Keyboard Shortcuts**:
- **Ctrl+Z**: Undo last action
- **Ctrl+Y**: Redo last undone action

**Menu**: Edit > Undo / Edit > Redo

---

## Complete Keyboard Shortcuts

### File Operations
- **Ctrl+O**: Open video file
- **Ctrl+E**: Export video
- **Ctrl+Q**: Quit application

### Edit Operations
- **Ctrl+Z**: Undo
- **Ctrl+Y**: Redo
- **Ctrl+T**: Toggle trim mode
- **I**: Set In point (trim start)
- **O**: Set Out point (trim end)

### Playback Control
- **Space**: Play/Pause
- **Left Arrow**: Seek backward 5s
- **Right Arrow**: Seek forward 5s
- **Up Arrow**: Volume up
- **Down Arrow**: Volume down
- **M**: Toggle mute (or add marker - context dependent)

### Markers
- **M**: Add marker at current position
- **[**: Jump to previous marker
- **]**: Jump to next marker

### View
- **F**: Toggle fullscreen
- **Escape**: Exit fullscreen
- **Ctrl+Shift+H**: Toggle high contrast mode

---

## Architecture Overview

### New Modules (Iteration 2)

```
src/
├── video/
│   ├── opencv_player.py      # (Iteration 1) OpenCV video player
│   ├── ffmpeg_processor.py   # (NEW) FFmpeg trim/export operations
│   ├── timeline.py            # (NEW) Multi-clip timeline data model
│   └── marker.py              # (NEW) Marker management
├── ui/
│   ├── main_window_opencv.py # (Iteration 1) Basic playback UI
│   ├── main_window_v2.py     # (NEW) Iteration 2 enhanced UI
│   ├── timeline_widget.py    # (NEW) Multi-clip timeline widget
│   └── export_dialog.py      # (NEW) Export settings dialog
└── utils/
    ├── theme_manager.py       # (NEW) High contrast theme
    └── command_stack.py       # (NEW) Undo/redo system
```

### Data Models

**Timeline**:
- Manages list of `TimelineClip` objects
- Handles clip ordering, insertion, deletion
- Emits signals for UI updates

**MarkerManager**:
- Stores `Marker` objects with time, label, color
- Supports navigation (prev/next)
- Persistent across video changes

**CommandStack**:
- Implements Command Pattern for undo/redo
- Tracks all reversible operations
- Max stack size: 100 commands

---

## Testing

### Manual Testing Checklist
See: `docs/iteration2/TESTING_CHECKLIST_ITERATION2.md`

### Cognitive Walkthrough Tasks
See: `docs/iteration2/cognitive_walkthrough_guide.md`

**3 Main Tasks**:
1. Trim a video clip (remove unwanted intro)
2. Combine multiple clips into one video
3. Mark important moments for navigation

---

## Known Limitations

### Current Iteration 2 Limitations

1. **No Audio with OpenCV Backend**
   - OpenCV doesn't support audio playback
   - Audio is preserved in exported videos (via FFmpeg)
   - Consider this a visual editing tool

2. **Timeline Playback Not Implemented**
   - Multi-clip timeline UI is complete
   - Playback across clips requires additional work
   - Can export multi-clip timeline to single video

3. **FFmpeg Required for Export**
   - Export features require FFmpeg installation
   - Application provides helpful error if missing
   - Manual installation needed

4. **Marker Labels Not Editable in UI**
   - Markers have default labels ("Marker 1", "Marker 2")
   - Labels can be edited in code but not via UI
   - Will be added in future iteration

5. **No Clip Trimming in Timeline**
   - Can trim source video before adding to timeline
   - Cannot trim clips after adding to timeline
   - Future feature: in-timeline trim handles

---

## Troubleshooting

### Issue: "FFmpeg not found" error

**Solution**:
1. Download FFmpeg from https://ffmpeg.org/download.html
2. Extract to `C:\ffmpeg` (or custom location)
3. Add to PATH:
   - Windows: System Properties > Environment Variables > Path > Add `C:\ffmpeg\bin`
   - Restart terminal/application
4. Verify: `ffmpeg -version`

### Issue: Video doesn't load

**Solution**:
- Check video codec (H.264 recommended)
- Try different video file
- Check console for error messages
- Ensure file path has no special characters

### Issue: Export takes very long

**Solution**:
- Lower quality preset (High → Medium)
- Video encoding is CPU-intensive
- Progress bar shows status
- Large videos (>100MB) may take 5-10 minutes

### Issue: High contrast mode text hard to read

**Solution**:
- Verify monitor brightness
- Yellow on black should be 19:1 contrast (AAA)
- If still difficult, report as bug with monitor specs

### Issue: Timeline clips not visible

**Solution**:
- Scroll down (timeline is in bottom splitter panel)
- Drag splitter divider to expand timeline area
- Click "+ Add Clip" to add first clip

---

## Accessibility Features

### WCAG 2.1 Compliance

- **Keyboard Navigation**: All features accessible without mouse
- **High Contrast Mode**: 19:1 contrast ratio (exceeds AAA)
- **Focus Indicators**: Visible cyan borders on focused elements
- **Alternative Input**: Keyboard shortcuts for all major functions

### Accessibility Testing

**Keyboard-Only Test**:
1. Unplug mouse
2. Use Tab to navigate between controls
3. Use Enter/Space to activate buttons
4. Verify all features accessible

**Screen Reader Test** (Future):
- All buttons should have text labels
- Tooltips provide additional context
- Current implementation basic, will improve

---

## HCI Principles Applied

### Fitts's Law
- **Large Targets**: Play/Pause button is 50x50px (most frequent action)
- **Central Placement**: Playback controls in center of bottom panel
- **Edge Targets**: Fullscreen button at edge for quick access

### Hick's Law
- **Limited Choices**: Export has only 3 quality options (not overwhelming)
- **Progressive Disclosure**: Advanced features hidden in menus
- **Grouped Actions**: Related commands in same menu (Edit menu has all trim functions)

### Gestalt Principles
- **Proximity**: Timeline clips grouped together visually
- **Similarity**: All markers use same flag shape
- **Continuity**: Timeline flows left-to-right (chronological)

### Nielsen's Heuristics
- **#1 Visibility of Status**: Status bar shows all major actions
- **#3 User Control**: Undo/redo for all editing operations
- **#5 Error Prevention**: Confirmation dialogs before destructive actions
- **#7 Flexibility**: Both keyboard shortcuts and buttons for common tasks
- **#10 Help & Documentation**: Tooltips on all controls

---

## Evaluation Plan

### Cognitive Walkthrough (Iteration 2)

**Participants**: 3-5 users (mix of novice/intermediate/advanced)

**Tasks**:
1. Trim video to remove unwanted section
2. Combine 3 clips into presentation
3. Mark 3 important moments with markers

**Metrics**:
- Task completion rate (target: >80%)
- Time on task (compared to baseline)
- Error count (mistakes during task)
- User satisfaction (5-point scale, target: >3.5)

**Documentation**: See `docs/iteration2/cognitive_walkthrough_guide.md`

---

## Future Work (Iteration 3)

Based on Iteration 2 feedback, planned for Iteration 3:

1. **Internationalization (i18n)**
   - English ↔ Chinese language switching
   - Qt translation system (.ts files)

2. **Timeline Playback**
   - Play across multiple clips seamlessly
   - Visual playhead indicator

3. **Enhanced Trim UI**
   - Visual trim handles on timeline
   - Drag to adjust trim range

4. **Marker Label Editing**
   - Double-click to edit marker labels
   - Color picker for custom marker colors

5. **Project Save/Load**
   - Save timeline state to file
   - Reload projects for continued editing

6. **Performance Optimization**
   - Faster seeking with frame caching
   - Reduced memory usage for long videos

7. **SUS Questionnaire**
   - System Usability Scale evaluation
   - Target score: >68 (above average)

---

## Credits

**Project**: XJCO2811 User Interfaces Assessment
**Institution**: University of Leeds
**Academic Year**: 2024-2025
**Iteration**: 2 of 3

**Technologies**:
- Python 3.8+
- PyQt5 5.15.10
- OpenCV 4.8.0+
- FFmpeg 4.4+

**References**:
- Nielsen, J. (1994). 10 Usability Heuristics
- WCAG 2.1 Guidelines (W3C)
- Wharton et al. (1994). Cognitive Walkthrough Method

---

## Support & Feedback

**Issues**: Report bugs or suggest features in GitHub Issues
**Documentation**: See `/docs` folder for detailed guides
**Testing**: Use `/docs/iteration2/TESTING_CHECKLIST_ITERATION2.md`

---

*Last Updated: 2025-11-26*
*Version: 2.0 (Iteration 2)*
