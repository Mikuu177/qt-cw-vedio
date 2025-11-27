# Iteration 2 - Video Editing Features & Enhanced Accessibility

## Overview

**Timeline**: Week 2-3
**Primary Goal**: Transform the video player into a full video editor with trimming, multi-clip assembly, and enhanced accessibility features.
**Evaluation Method**: Cognitive Walkthrough (task-based usability testing)

## Key Features to Implement

### 1. Video Trimming/Cutting 🎬

**User Story**: As a teacher (Dr. Sarah Chen), I need to trim lecture recordings to remove unnecessary content before sharing with students.

**Technical Implementation**:
- Use FFmpeg for actual video processing
- UI components:
  - Trim mode button to enter editing mode
  - In/Out point markers on timeline
  - Visual trim range indicator
  - Trim preview (show selected segment)
- Keyboard shortcuts:
  - `I`: Set In point
  - `O`: Set Out point
  - `Shift+Delete`: Delete selected segment
  - `Ctrl+T`: Trim to selection

**HCI Principles Applied**:
- **Feedback**: Visual markers show trim points clearly
- **Error Prevention**: Confirm before destructive operations
- **Reversibility**: Undo/redo for trim operations

### 2. Multi-Clip Timeline Assembly 📽️

**User Story**: As a student (Alex Martinez), I need to combine multiple video clips into a single presentation.

**Technical Implementation**:
- Timeline data model:
  ```python
  class TimelineClip:
      def __init__(self, source_path, start_time, duration, position):
          self.source_path = source_path
          self.start_time = start_time  # Trim start in source
          self.duration = duration
          self.position = position  # Position on timeline

  class Timeline:
      def __init__(self):
          self.clips = []  # List of TimelineClip objects

      def add_clip(self, clip):
          # Insert clip at position, shift others if needed

      def remove_clip(self, clip_id):
          # Remove and close gap
  ```

- UI components:
  - Multi-track timeline view (bottom panel)
  - Clip thumbnails with duration labels
  - Drag-and-drop to reorder clips
  - Add clip button (+)
  - Delete clip button (X)
  - Gap visualization between clips

**HCI Principles Applied**:
- **Direct Manipulation**: Drag clips to reorder
- **Gestalt (Proximity)**: Group clip controls together
- **Consistency**: Follow video editing conventions (Premiere, Final Cut)

### 3. Marker System 📍

**User Story**: As an amateur editor (Robert Williams), I need to mark important moments to quickly navigate long videos.

**Technical Implementation**:
- Marker data structure:
  ```python
  class Marker:
      def __init__(self, time_ms, label, color):
          self.time_ms = time_ms
          self.label = label
          self.color = color  # For different marker types
  ```

- UI components:
  - Marker indicators on timeline (colored flags)
  - Add marker button (M key)
  - Marker list panel (sidebar)
  - Click marker to jump to position
  - Edit marker label (double-click)
  - Delete marker (right-click menu)

**HCI Principles Applied**:
- **Recognition over Recall**: Visual markers reduce memory load
- **Flexibility**: Multiple marker colors for categorization
- **Efficiency**: Quick navigation for power users

### 4. High Contrast Mode 🎨

**User Story**: As a visually impaired user, I need high contrast UI to see controls clearly.

**Technical Implementation**:
- Qt StyleSheets for theme switching:
  ```python
  class ThemeManager:
      NORMAL_THEME = """
          QMainWindow { background-color: #f0f0f0; }
          QPushButton { background-color: #e0e0e0; color: #000; }
          ...
      """

      HIGH_CONTRAST_THEME = """
          QMainWindow { background-color: #000000; }
          QPushButton {
              background-color: #000000;
              color: #FFFF00;
              border: 2px solid #FFFFFF;
              font-weight: bold;
          }
          QSlider::handle { background: #FFFF00; }
          ...
      """

      def apply_theme(self, theme_name):
          # Apply stylesheet to application
  ```

- UI components:
  - Toggle button in View menu
  - Keyboard shortcut: `Ctrl+Shift+H`
  - Persist preference in settings

**WCAG 2.1 Compliance**:
- Text contrast ratio: Minimum 7:1 (Level AAA)
- Button borders: 3:1 contrast with background
- Focus indicators: Visible keyboard focus outline

### 5. Export Functionality 💾

**User Story**: After editing, I need to save my work as a new video file.

**Technical Implementation**:
- FFmpeg export pipeline:
  ```python
  def export_timeline(timeline, output_path, quality):
      # Generate FFmpeg filter complex for:
      # - Concatenating clips
      # - Applying trims
      # - Re-encoding with quality settings

      # Quality presets:
      # - High: H.264, CRF 18, 1080p
      # - Medium: H.264, CRF 23, 720p
      # - Low: H.264, CRF 28, 480p
  ```

- UI components:
  - Export dialog with preview
  - Quality dropdown (High/Medium/Low)
  - Output path selector
  - Progress bar with ETA
  - Cancel button

**HCI Principles Applied**:
- **Visibility of Status**: Progress bar shows export status
- **User Control**: Cancel anytime
- **Error Recovery**: Retry on failure

### 6. Enhanced Keyboard Shortcuts ⌨️

Expand keyboard support for editing operations:

| Shortcut | Action |
|----------|--------|
| `Ctrl+N` | New project |
| `Ctrl+S` | Save project |
| `Ctrl+E` | Export video |
| `I` | Set In point |
| `O` | Set Out point |
| `M` | Add marker |
| `Ctrl+Z` | Undo |
| `Ctrl+Y` | Redo |
| `Delete` | Delete selected clip |
| `Ctrl+D` | Duplicate clip |
| `[` | Jump to previous marker |
| `]` | Jump to next marker |

## Architecture Changes

### New Modules

```
src/
├── video/
│   ├── opencv_player.py (existing)
│   ├── ffmpeg_processor.py (NEW) - Trim, export operations
│   ├── timeline.py (NEW) - Timeline data model
│   └── marker.py (NEW) - Marker management
├── ui/
│   ├── main_window_opencv.py (existing, will extend)
│   ├── timeline_widget.py (NEW) - Multi-clip timeline UI
│   ├── trim_controls.py (NEW) - Trim mode UI
│   ├── marker_panel.py (NEW) - Marker list sidebar
│   └── export_dialog.py (NEW) - Export settings dialog
└── utils/
    ├── theme_manager.py (NEW) - High contrast mode
    └── command_stack.py (NEW) - Undo/redo (Command pattern)
```

### Data Persistence

Use SQLite to save project state:

```sql
CREATE TABLE projects (
    id INTEGER PRIMARY KEY,
    name TEXT,
    created_at TIMESTAMP,
    modified_at TIMESTAMP
);

CREATE TABLE timeline_clips (
    id INTEGER PRIMARY KEY,
    project_id INTEGER,
    source_path TEXT,
    start_time_ms INTEGER,
    duration_ms INTEGER,
    position_ms INTEGER,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

CREATE TABLE markers (
    id INTEGER PRIMARY KEY,
    project_id INTEGER,
    time_ms INTEGER,
    label TEXT,
    color TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);
```

## Cognitive Walkthrough Evaluation Plan

### Task Scenarios

**Task 1: Trim a Video**
1. Open a video file
2. Play to find unwanted section
3. Set In point before unwanted section
4. Set Out point after unwanted section
5. Delete marked section
6. Preview result

**Task 2: Combine Multiple Clips**
1. Create new project
2. Add first video clip
3. Add second video clip
4. Reorder clips by dragging
5. Preview combined result
6. Export final video

**Task 3: Mark Important Moments**
1. Open a long video
2. Play and identify 3 key moments
3. Add markers at each moment
4. Label markers descriptively
5. Use markers to navigate

### Evaluation Metrics
- **Task completion rate**: % of users who complete task
- **Time on task**: Average time to complete
- **Error count**: Wrong actions taken
- **User satisfaction**: 5-point Likert scale

### Participants
- 3-5 users with varying experience:
  - 1-2 novices (never used video editor)
  - 2-3 intermediate (used basic editors like Windows Photos)
  - 1 expert (familiar with Premiere/Final Cut)

## HCI Theory Integration

### Fitts's Law
- **Large targets**: Trim markers ≥44px touch target
- **Central placement**: Most-used buttons near video player

### Hick's Law
- **Limited choices**: Export dialog has 3 quality options (not 10)
- **Progressive disclosure**: Advanced settings hidden by default

### Gestalt Principles
- **Proximity**: Group timeline controls together
- **Similarity**: All markers use same shape (flag icon)
- **Continuity**: Timeline flows left-to-right

### Error Prevention (Nielsen Heuristic #5)
- **Confirmation dialogs**: Before deleting clips or overwriting files
- **Undo/redo**: All editing actions reversible
- **Auto-save**: Project state saved every 2 minutes

### Accessibility (WCAG 2.1 Level AA)
- **Keyboard navigation**: All functions accessible via keyboard
- **Focus indicators**: 3px yellow outline on focused elements
- **Color independence**: Don't rely solely on color (use icons + text)
- **High contrast mode**: 7:1 contrast ratio for text

## Testing Checklist

### Video Trimming
- [ ] Set In point at correct frame
- [ ] Set Out point at correct frame
- [ ] Visual trim range highlighted
- [ ] Delete trimmed section
- [ ] Undo trim operation
- [ ] Redo trim operation

### Multi-Clip Timeline
- [ ] Add multiple clips to timeline
- [ ] Drag to reorder clips
- [ ] Click clip to select
- [ ] Delete selected clip
- [ ] Play across clip boundaries (smooth transition)
- [ ] Export multi-clip timeline

### Marker System
- [ ] Add marker at current position
- [ ] Edit marker label
- [ ] Delete marker
- [ ] Click marker to jump
- [ ] Markers persist after closing
- [ ] Keyboard shortcuts work (M, [, ])

### High Contrast Mode
- [ ] Toggle high contrast (menu + keyboard)
- [ ] All text readable (7:1 contrast)
- [ ] Button borders visible
- [ ] Focus indicators work
- [ ] Preference saved after restart

### Export
- [ ] Export single clip
- [ ] Export multi-clip timeline
- [ ] Quality settings applied correctly
- [ ] Progress bar updates
- [ ] Cancel export mid-process
- [ ] Output file playable in VLC

### Accessibility
- [ ] All features accessible via keyboard
- [ ] Tab order logical
- [ ] Screen reader announces button labels
- [ ] High contrast mode works with all features

## Implementation Timeline

### Week 2 (Days 1-4)
- **Day 1**: FFmpeg integration and trim functionality
- **Day 2**: Multi-clip timeline data model and UI
- **Day 3**: Marker system
- **Day 4**: High contrast mode

### Week 3 (Days 5-7)
- **Day 5**: Export functionality
- **Day 6**: Undo/redo system and project save/load
- **Day 7**: Testing and bug fixes

### Week 3 (Days 8-10)
- **Day 8**: Prepare cognitive walkthrough materials
- **Day 9**: Conduct evaluations with 3-5 participants
- **Day 10**: Document findings and create Iteration 2 video

## Success Criteria

✅ **Code Complete**:
- All 6 features implemented and tested
- No critical bugs
- Smooth performance (no lag when editing)

✅ **Documentation Complete**:
- Cognitive walkthrough report written
- Feedback integration plan documented
- Iteration 2 video produced (45s-1m20s)

✅ **Evaluation Complete**:
- 3+ participants evaluated
- Task completion rate >80%
- User satisfaction >3.5/5
- Issues identified and prioritized for Iteration 3

## Risks and Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| FFmpeg complexity | High | Start with simple trim, test early |
| Timeline UI performance | Medium | Use efficient rendering (only visible area) |
| Cognitive walkthrough recruitment | Medium | Over-recruit (5 participants for 3 needed) |
| Export takes too long | Low | Show progress bar, allow background export |

## References

- Nielsen, J. (1994). 10 Usability Heuristics
- WCAG 2.1 Guidelines: https://www.w3.org/WAI/WCAG21/quickref/
- FFmpeg Documentation: https://ffmpeg.org/ffmpeg.html
- Cognitive Walkthrough Method: Wharton et al. (1994)
- Qt Documentation: https://doc.qt.io/qt-5/

---

*Document Version: 1.0*
*Last Updated: 2025-11-26*
*Status: Ready for Implementation*
