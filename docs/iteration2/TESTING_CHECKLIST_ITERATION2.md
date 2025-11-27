# Video Editor/Player - Iteration 2 Testing Checklist

## Testing Overview

**Iteration**: 2
**Testing Date**: 2025-11-26
**Features Added**: Video editing, multi-clip timeline, markers, trim/cut, export, high contrast mode, undo/redo
**Evaluation Method**: Cognitive Walkthrough (task-based)

---

## 1. Video Trimming/Cutting ✂️

### Trim Mode Activation
- [ ] **Ctrl+T** - Toggle trim mode ON
- [ ] **Status bar** - Shows "Trim mode: Press I for In point, O for Out point"
- [ ] **Ctrl+T** again - Toggle trim mode OFF

### Set In/Out Points
- [ ] **I Key** - Set In point at current position
- [ ] **In point label** - Displays "In: MM:SS" in green
- [ ] **O Key** - Set Out point at current position
- [ ] **Out point label** - Displays "Out: MM:SS" in red
- [ ] **Timeline visual** - Trim range highlighted (if implemented)

### Trim Operations
- [ ] **Menu: Edit > Clear Trim Points** - Clears both In and Out points
- [ ] **Labels cleared** - In/Out labels disappear
- [ ] **Set In before Out** - Works correctly
- [ ] **Set Out before In** - Works correctly (handles reverse order)

### FFmpeg Integration
- [ ] **FFmpeg check** - Application detects if FFmpeg is installed
- [ ] **Error message** - Shows warning if FFmpeg not available

---

## 2. Multi-Clip Timeline Assembly 🎬

### Add Clips to Timeline
- [ ] **+ Add Clip button** - Opens file dialog
- [ ] **Select video file** - Adds clip to timeline
- [ ] **Clip widget created** - Shows filename and duration
- [ ] **Multiple clips** - Can add 3+ clips successfully
- [ ] **Timeline info** - Shows "N clip(s) | Total duration: X.Xs"

### Clip Selection
- [ ] **Click clip** - Clip becomes selected (highlighted border)
- [ ] **Previous selection** - Deselected when new clip clicked
- [ ] **Selection visual** - Clear blue border on selected clip

### Clip Deletion
- [ ] **Right-click clip** - Shows context menu with "Delete Clip"
- [ ] **Delete Clip** - Clip removed from timeline
- [ ] **Undo deletion** - Ctrl+Z restores deleted clip
- [ ] **Clear Timeline button** - Confirmation dialog appears
- [ ] **Confirm clear** - All clips removed from timeline

### Clip Reordering (Drag-and-Drop)
- [ ] **Drag clip** - Visual feedback during drag
- [ ] **Drop clip** - Clip reordered in timeline
- [ ] **Timeline recalculation** - Positions updated correctly
- [ ] **Undo reorder** - Ctrl+Z restores original order

### Timeline Playback (Future)
- [ ] **Play timeline** - Plays first clip (basic implementation)
- Note: Full multi-clip playback requires additional implementation

---

## 3. Marker System 📍

### Add Markers
- [ ] **M Key** - Adds marker at current position
- [ ] **Status bar** - Shows "Marker added at MM:SS"
- [ ] **Marker bar** - Marker appears as colored flag
- [ ] **Default label** - "Marker N" assigned automatically
- [ ] **Default color** - Cycles through colors (red, blue, green, etc.)

### Marker Navigation
- [ ] **Click marker** - Jumps video to marker position
- [ ] **[ Key** - Jump to previous marker
- [ ] **] Key** - Jump to next marker
- [ ] **First marker** - [ key does nothing
- [ ] **Last marker** - ] key does nothing
- [ ] **Status bar feedback** - Shows "Jumped to marker: [label]"

### Marker Management
- [ ] **Marker tooltip** - Hover shows label and time
- [ ] **Multiple markers** - Can add 5+ markers
- [ ] **Marker persistence** - Markers remain after pause/seek
- [ ] **Timeline clear** - Markers persist after timeline cleared

### Undo/Redo Markers
- [ ] **Undo add marker** - Ctrl+Z removes last marker
- [ ] **Redo add marker** - Ctrl+Y restores marker

---

## 4. High Contrast Mode (Accessibility) 🎨

### Toggle High Contrast
- [ ] **Menu: View > High Contrast Mode** - Toggles mode
- [ ] **Ctrl+Shift+H** - Keyboard shortcut works
- [ ] **Status bar** - Shows "High contrast mode enabled/disabled"

### High Contrast Theme (WCAG 2.1 AAA)
- [ ] **Background** - Black (#000000)
- [ ] **Text** - Yellow (#FFFF00) or White (#FFFFFF)
- [ ] **Buttons** - Yellow text, white borders (3px)
- [ ] **Hover state** - Yellow border on hover
- [ ] **Focus indicators** - Cyan border (4px) on focus
- [ ] **Sliders** - Yellow handles, white borders
- [ ] **ComboBoxes** - Yellow text, white borders

### Contrast Ratios (Use Contrast Checker Tool)
- [ ] **Yellow/Black** - ≥ 19:1 (exceeds AAA requirement of 7:1) ✅
- [ ] **White/Black** - 21:1 (maximum contrast) ✅
- [ ] **Button borders** - ≥ 3:1 with background ✅
- [ ] **All text readable** - No strain to read

### Theme Persistence
- [ ] **Close and reopen app** - High contrast preference saved
- [ ] **Settings file** - Preference stored in QSettings

### Return to Normal Theme
- [ ] **Toggle off** - Normal theme restored
- [ ] **All controls** - Return to normal styling
- [ ] **No visual artifacts** - Clean transition

---

## 5. Export Functionality 💾

### Export Dialog
- [ ] **Menu: File > Export Video** - Opens export dialog
- [ ] **Ctrl+E shortcut** - Opens export dialog
- [ ] **Dialog title** - "Export Video"

### Output File Selection
- [ ] **Browse button** - Opens save file dialog
- [ ] **Select path** - Path shown in text field
- [ ] **Auto .mp4 extension** - Added if not provided

### Quality Presets
- [ ] **High quality** - "High (1080p, CRF 18)" selected
- [ ] **Medium quality** - "Medium (720p, CRF 23)" option
- [ ] **Low quality** - "Low (480p, CRF 28)" option
- [ ] **Quality info** - Description updates when changed

### Export Process
- [ ] **Export button** - Disabled if no output path
- [ ] **Start export** - Progress bar appears
- [ ] **Progress updates** - Bar shows 0-100%
- [ ] **Status message** - Shows export status
- [ ] **File overwrite** - Confirmation dialog if file exists

### Export Completion
- [ ] **Success message** - "Export completed" dialog
- [ ] **Output file exists** - File created at specified path
- [ ] **Output playable** - Can play in VLC or Windows Media Player
- [ ] **Quality correct** - Resolution matches selected preset

### Cancel Export
- [ ] **Cancel button** - Stops export process
- [ ] **Cleanup** - Partial files removed

---

## 6. Undo/Redo System ↩️

### Undo Operations
- [ ] **Ctrl+Z** - Undo last action
- [ ] **Menu: Edit > Undo** - Same functionality
- [ ] **Undo disabled** - When nothing to undo
- [ ] **Undo add clip** - Removes last added clip
- [ ] **Undo remove clip** - Restores removed clip
- [ ] **Undo add marker** - Removes last marker

### Redo Operations
- [ ] **Ctrl+Y** - Redo last undone action
- [ ] **Menu: Edit > Redo** - Same functionality
- [ ] **Redo disabled** - When nothing to redo
- [ ] **Redo after undo** - Restores undone action

### Undo/Redo Stack
- [ ] **Multiple undos** - Can undo 5+ actions in sequence
- [ ] **Multiple redos** - Can redo all undone actions
- [ ] **New action clears redo** - Redo stack cleared after new action
- [ ] **Stack limit** - No crash with 100+ actions

---

## 7. Enhanced Keyboard Shortcuts ⌨️

| Shortcut | Action | Status |
|----------|--------|--------|
| **Ctrl+O** | Open video file | [ ] |
| **Ctrl+E** | Export video | [ ] |
| **Ctrl+Z** | Undo | [ ] |
| **Ctrl+Y** | Redo | [ ] |
| **Ctrl+T** | Toggle trim mode | [ ] |
| **I** | Set In point | [ ] |
| **O** | Set Out point | [ ] |
| **M** | Add marker | [ ] |
| **[** | Previous marker | [ ] |
| **]** | Next marker | [ ] |
| **F** | Fullscreen | [ ] |
| **Ctrl+Shift+H** | Toggle high contrast | [ ] |
| **Space** | Play/Pause | [ ] |
| **Left Arrow** | Seek backward 5s | [ ] |
| **Right Arrow** | Seek forward 5s | [ ] |
| **Up Arrow** | Volume up | [ ] |
| **Down Arrow** | Volume down | [ ] |
| **Escape** | Exit fullscreen | [ ] |
| **Ctrl+Q** | Quit | [ ] |

---

## 8. UI/UX Quality (HCI Principles)

### Fitts's Law (Target Sizes)
- [ ] **Play/Pause button** - 50x50px (large, central)
- [ ] **Other buttons** - ≥ 40x40px
- [ ] **Touch targets** - ≥ 44px (iOS guideline)

### Hick's Law (Choice Limitation)
- [ ] **Export quality** - Only 3 options (not overwhelming)
- [ ] **Speed control** - 7 preset options (manageable)
- [ ] **Menu structure** - Logical grouping (File, Edit, View, Markers)

### Gestalt Principles
- [ ] **Proximity** - Related controls grouped (playback buttons together)
- [ ] **Similarity** - All markers use same flag shape
- [ ] **Continuity** - Timeline flows left-to-right

### Feedback (Nielsen Heuristic #1)
- [ ] **All button clicks** - Visual feedback (pressed state)
- [ ] **Status bar** - Updates for every major action
- [ ] **Progress indicators** - For long operations (export)
- [ ] **Tooltips** - On all buttons

### Error Prevention (Nielsen Heuristic #5)
- [ ] **Delete confirmation** - For destructive actions
- [ ] **File overwrite confirmation** - Before exporting
- [ ] **Undo available** - For all editing operations

### Consistency (Nielsen Heuristic #4)
- [ ] **Standard icons** - Qt system icons used
- [ ] **Keyboard shortcuts** - Follow platform conventions (Ctrl+Z, Ctrl+Y)
- [ ] **Menu structure** - Follows standard app patterns

---

## 9. Accessibility (WCAG 2.1 Level AA)

### Keyboard Navigation
- [ ] **Tab order** - Logical flow through controls
- [ ] **All features accessible** - No mouse-only operations
- [ ] **Focus indicators** - Visible on all focusable elements

### Visual Accessibility
- [ ] **High contrast mode** - Available and functional
- [ ] **Color independence** - Don't rely solely on color (use text labels)
- [ ] **Font size** - Readable (≥ 10pt)

### Screen Reader Support (Future)
- [ ] **Button labels** - All buttons have text or aria-labels
- [ ] **Tooltips** - Provide additional context

---

## 10. Performance & Stability

### Video Playback
- [ ] **Smooth playback** - No stuttering
- [ ] **Seek responsive** - < 500ms seek time
- [ ] **Timeline scrub** - Smooth preview

### Memory Management
- [ ] **Multiple clips loaded** - No memory leaks
- [ ] **Export completion** - Memory released
- [ ] **Long session** - Stable after 30+ minutes

### Error Handling
- [ ] **Invalid video file** - Error message shown
- [ ] **FFmpeg not found** - Graceful degradation
- [ ] **Export failure** - Error reported to user

### Cross-Platform (Windows Focus)
- [ ] **Windows 10** - All features work
- [ ] **Windows 11** - All features work
- [ ] **File paths** - Handle Windows paths correctly

---

## 11. Integration Testing

### Combined Workflows
- [ ] **Load video → Set markers → Export** - Full workflow
- [ ] **Load video → Trim → Add to timeline → Export** - Edit workflow
- [ ] **Multiple clips → Reorder → Export** - Multi-clip workflow

### State Management
- [ ] **Save/Load project** - (If implemented) Settings persist
- [ ] **Markers persist** - Across video changes
- [ ] **Theme preference** - Saved and restored

---

## Known Issues & Limitations

### ⚠️ Expected Behaviors
1. **No Audio Playback**: OpenCV backend doesn't support audio (documented limitation)
2. **FFmpeg Required**: Export requires FFmpeg installation
3. **Single Video Playback**: Timeline can hold multiple clips but playback is single-video only (will be enhanced in future)

### 🐛 Bugs to Fix (If Found)
- [ ] List any bugs discovered during testing
- [ ] Prioritize by severity (Critical, High, Medium, Low)

---

## Cognitive Walkthrough Tasks

### Task 1: Trim a Video
**Scenario**: Remove unwanted intro from lecture recording

1. [ ] Open video file
2. [ ] Play to find unwanted section (0:00-0:15)
3. [ ] Set In point at 0:15
4. [ ] Set Out point at video end
5. [ ] Menu > Edit > Trim (if implemented) OR use FFmpeg export
6. [ ] Verify result

**Success Criteria**: User completes task without errors in < 3 minutes

### Task 2: Combine Multiple Clips
**Scenario**: Create presentation from multiple videos

1. [ ] Click "+ Add Clip" button
2. [ ] Select first video file
3. [ ] Click "+ Add Clip" again
4. [ ] Select second video file
5. [ ] Verify both clips in timeline
6. [ ] (Optional) Reorder by dragging
7. [ ] Export combined video

**Success Criteria**: User understands timeline concept, completes in < 5 minutes

### Task 3: Mark Important Moments
**Scenario**: Navigate long lecture video

1. [ ] Open long video (> 5 minutes)
2. [ ] Play and identify 3 key moments
3. [ ] Press M at each moment
4. [ ] Verify markers appear
5. [ ] Use [ and ] to navigate markers
6. [ ] Verify jumps to correct positions

**Success Criteria**: User finds marker navigation useful, completes in < 4 minutes

---

## Testing Environment

- **OS**: Windows 11 / Windows 10
- **Python**: 3.8+
- **PyQt5**: 5.15.10
- **OpenCV**: 4.12.0+
- **FFmpeg**: 4.4+ (if installed)
- **Test Videos**: Various formats (MP4, AVI, MKV)

---

## Test Results Summary

### Features Implemented
- [x] Video trimming (In/Out points)
- [x] Multi-clip timeline UI
- [x] Marker system
- [x] High contrast mode
- [x] Export dialog
- [x] Undo/Redo system

### Features Partially Implemented
- [ ] FFmpeg trim/export (requires FFmpeg installation and integration)
- [ ] Multi-clip playback (UI ready, playback logic pending)

### Test Pass Rate
- **Manual Tests**: ___ / ___ passed (__%)
- **Cognitive Walkthrough**: ___ / 3 tasks completed successfully

---

*Testing Date: 2025-11-26*
*Tester: [Your Name]*
*Test Duration: [Duration]*
*Overall Assessment: [Pass/Fail/Needs Improvement]*
