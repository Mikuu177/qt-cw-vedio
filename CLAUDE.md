# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Context

This is an **academic assessment project** for XJCO2811 User Interfaces at the University of Leeds. The goal is to build a video editor/player based on the Tomeo application framework, demonstrating the complete interaction design lifecycle.

**Submission Deadline**: 04/12/2025 10:00 PM (China time)

## Assessment-Specific Constraints

### Critical Requirements
1. **Three Iteration Cycles Required**: The project MUST go through exactly 3 iterations, each with:
   - Specific evaluation methodology (Heuristic Evaluation → Cognitive Walkthrough → SUS Questionnaire)
   - Documentation of findings
   - Integration of feedback into next iteration
   - Iteration video (45s-1m20s)

2. **Evaluation Methods Are Fixed**:
   - Iteration 1: Heuristic Evaluation (Nielsen's 10 heuristics)
   - Iteration 2: Cognitive Walkthrough (task-based)
   - Iteration 3: SUS Questionnaire (quantitative)

3. **Mandatory Deliverables**:
   - Working prototype (must be stable, no crashes)
   - 6-page academic report (structured: Intro, Theory, Method, Results, Discussion, Conclusion)
   - 4 videos: 3 iteration videos (45s-1m20s each) + 1 showcase (1m-1m30s)
   - Ethics documentation (consent forms, privacy protocols)
   - All videos must have subtitles (accessibility requirement)

4. **Academic Writing Standards**:
   - Must cite UI/UX theory from course materials
   - Apply HCI principles explicitly (Fitts's Law, Hick's Law, Gestalt, WCAG 2.1)
   - Link design decisions to theoretical framework
   - Use proper academic citations

### Scope Boundaries
- **This is NOT a social media app**: Do not add features like comments, likes, user profiles, cloud storage
- **Focus on editing AND playback**: The title is "video editor/player" - both aspects required
- **Based on Tomeo**: Improvements should build on existing Tomeo application patterns
- **Accessibility is mandatory**: Keyboard shortcuts, high contrast mode, screen reader support
- **Internationalization required**: Minimum English + Chinese support

## Project Architecture

### High-Level Structure
```
qt-cw-vedio/
├── src/              # Application source code
│   ├── ui/          # Qt UI components (widgets, windows, dialogs)
│   ├── video/       # Video processing (playback, editing, FFmpeg integration)
│   └── utils/       # Helper functions, utilities
├── docs/            # All documentation
│   ├── iteration1/  # Week 1-2: Scenarios, lo-fi prototypes, heuristic evaluation
│   ├── iteration2/  # Week 2-3: Hi-fi prototype, accessibility, cognitive walkthrough
│   ├── iteration3/  # Week 3-4: Final features, i18n, SUS questionnaire
│   ├── ethics/      # Consent forms, privacy docs
│   └── final_report/ # 6-page academic report
├── prototypes/      # Figma/Adobe XD files, wireframes
└── videos/          # 4 demonstration videos
```

### Technology Decisions
- **UI Framework**: Qt (C++ or PyQt) - must follow Qt conventions
- **Video Playback**: QMediaPlayer for basic playback
- **Video Editing**: FFmpeg for trim/cut/export operations
- **Data Persistence**: SQLite for user preferences and project state
- **i18n**: Qt's built-in translation system (.ts files)

### Key Architectural Patterns
1. **Separation of Concerns**:
   - UI components should NOT directly manipulate video files
   - Video processing logic isolated in `/video` module
   - Use signals/slots (Qt) or callbacks for UI ↔ logic communication

2. **Undo/Redo System**:
   - Implement Command Pattern for all editing operations
   - Required for Iteration 3

3. **Timeline Data Structure**:
   - Central data model for multi-clip assembly
   - Stores clip references, trim points, transitions
   - Notifies UI of changes

## Development Workflow

### When Implementing Features
1. **Always tie to scenarios**: Each feature should map to one of the 3 user scenarios (teacher/student/amateur)
2. **Document design rationale**: Explain WHY using UI/UX theory (for report writing)
3. **Consider accessibility from start**: Don't add it as afterthought
4. **Think about evaluation**: How will this feature be evaluated? What tasks will users perform?

### Iteration-Specific Focus

#### Iteration 1 (Current/Next Phase)
**Primary Goal**: Establish foundation
- Create 3 detailed user scenarios (write in `/docs/iteration1/scenarios.md`)
- Implement basic video playback (play, pause, seek, timeline)
- Build minimal UI framework
- Conduct heuristic evaluation with 3-5 participants
- Document in `/docs/iteration1/evaluation1_report.md`

**Code Focus**: Get video playing with basic controls. UI can be simple but must follow Nielsen's heuristics.

#### Iteration 2
**Primary Goal**: Add editing capabilities + accessibility
- Implement trim/cut using FFmpeg
- Multi-clip timeline assembly
- Keyboard shortcuts for all major functions
- High contrast mode toggle
- Cognitive walkthrough evaluation (task: "trim a video clip")

**Code Focus**: FFmpeg integration is complex - allocate time for this.

#### Iteration 3
**Primary Goal**: Polish and finalize
- Complete i18n (English ↔ Chinese switching)
- Performance optimization (smooth playback, responsive UI)
- Export functionality
- SUS questionnaire with 5-10 users
- Calculate and report SUS score (industry standard: >68 is above average)

**Code Focus**: No new major features. Bug fixes, optimization, i18n.

## Documentation Requirements

### For Each Iteration
Create these files in `/docs/iterationN/`:
- `scenarios.md` (Iteration 1 only): 3 detailed user scenarios
- `evaluationN_report.md`: Full evaluation writeup including:
  - Methodology chosen and rationale
  - Participant demographics (anonymized)
  - Findings (tables, screenshots)
  - Severity ratings or task completion rates
  - Decisions made (accept/modify/reject feedback)
- `feedback_integration.md` (Iterations 2-3): How previous evaluation changed design

### Video Production Notes
- **Iteration videos**: Show the PROCESS (code, design decisions, evaluation setup)
- **Showcase video**: Show the PRODUCT (for non-technical audience, business presentation style)
- All must have subtitles (use `.srt` files or burned-in)
- Length is STRICT: will lose marks if outside specified ranges

### Academic Report Structure
The 6-page report must follow this structure exactly:
1. **Introduction** (1 page): Context, goals, Tomeo improvements
2. **Theoretical Framework** (1.5 pages): HCI principles applied, citations
3. **Methodology** (1 page): Scenarios, prototyping, evaluation methods + rationale
4. **Results** (1.5 pages): Findings from 3 iterations
5. **Discussion** (0.5 pages): Theory ↔ practice connections
6. **Conclusion** (0.5 pages): Achievements, limitations, future work

Include references! Cite Nielsen Norman Group, WCAG, Qt docs, course materials.

## Ethics Compliance

### Before ANY User Evaluation
Must have in `/docs/ethics/`:
- `informed_consent_template.md`: Participants sign before evaluation
- `participant_information_sheet.md`: Explains study purpose, data usage
- `data_privacy_protocol.md`: How data is stored/anonymized/deleted
- `anonymization_procedures.md`: Procedure for removing identifying info

### Rules
- Never use real names in reports (use P1, P2, P3...)
- Get written consent before recording video/audio
- Store evaluation data securely, delete after assessment
- No personally identifying information in GitHub repository

## UI/UX Theory Application

### Must Explicitly Apply These Principles
1. **Fitts's Law**: Make play/pause button large and central (frequent action)
2. **Hick's Law**: Limit menu choices, use progressive disclosure for advanced features
3. **Gestalt Principles**: Group related timeline controls visually
4. **Consistency**: Follow Qt platform conventions (standard icons, layouts)
5. **Feedback**: Visual confirmation of all user actions (e.g., trim markers appear on timeline)
6. **Error Prevention**: Confirm before destructive actions, provide undo
7. **WCAG 2.1 AA**: Color contrast ratios, keyboard navigation, alt text

### When Adding Any UI Element, Ask
- Which HCI principle does this apply?
- How does this support the user scenarios?
- Is it accessible (keyboard + screen reader)?
- Will it work in both English and Chinese?

## Common Pitfalls to Avoid

1. **Don't skip iterations**: Each iteration must have distinct evaluation and improvements
2. **Don't write generic report**: Must cite specific theory and tie to design decisions
3. **Don't ignore accessibility**: It's explicitly in marking criteria (3 marks for UI quality includes accessibility)
4. **Don't forget subtitles on videos**: Accessibility requirement
5. **Don't add social features**: This is video editing, not social media
6. **Don't make videos too long or short**: Strict time limits in marking rubric
7. **Don't use placeholder buttons**: Marking criteria: "All buttons work or some just preview?" (2 marks)

## Marking Criteria Priorities

### For First-Class Mark (>70)
- **Prototype**: Stable + complete + responsive/accessible UI + **several** creative improvements beyond Tomeo
- **Report**: Theory clearly explained and **explicitly linked** to project decisions
- **Videos**: Clear, professional, not cluttered, shows process evolution
- **Evaluations**: Methodology applied to "very high standard"

### Quick Wins for High Marks
- Make UI responsive to window resizing (marks for "responsive" UI)
- Add comprehensive keyboard shortcuts (accessibility + power users)
- Document every design decision with theory rationale (for report)
- Over-recruit evaluation participants (backup if some cancel)
- Practice video creation early (quality matters)

## Current Project Status (Updated: 2025-11-26)

### ✅ Completed - Iteration 1 Foundation

#### Code Implementation
- ✅ **OpenCV-based video player** (better codec support than QMediaPlayer)
  - Smooth video playback with proper frame timing
  - Timeline scrubbing and seeking
  - Time display (current/total in MM:SS format)

- ✅ **Enhanced playback controls**
  - Play, Pause, Stop buttons
  - Fast-forward (+10s) and Rewind (-10s) buttons
  - Variable playback speed (0.25x, 0.5x, 0.75x, 1x, 1.25x, 1.5x, 2x)
  - Volume control with visual indicator
  - Mute button with icon toggle

- ✅ **Display features**
  - Fullscreen mode (F key or button)
  - Responsive video widget
  - Status bar feedback
  - Auto-load sample video for testing

- ✅ **Accessibility**
  - Comprehensive keyboard shortcuts:
    - Space: Play/Pause
    - Left/Right arrows: Seek ±5s
    - Up/Down arrows: Volume control
    - F: Fullscreen toggle
    - M: Mute toggle
    - Escape: Exit fullscreen
    - Ctrl+O: Open file
    - Ctrl+Q: Quit
  - Tooltip hints on all buttons
  - Clear visual feedback

#### Documentation
- ✅ **User scenarios document** (`docs/iteration1/scenarios.md`)
  - 3 detailed scenarios: Teacher, Student, Amateur
  - Pain points and goals identified
  - Design implications mapped to HCI principles

- ✅ **Scoping analysis** (`docs/iteration1/scoping_analysis.md`)
  - MoSCoW prioritization for all 3 iterations
  - Technical feasibility assessment
  - Risk management plan
  - Resource allocation

#### Technical Stack Confirmed
- **Backend**: OpenCV for video decoding (resolves Windows codec issues)
- **UI**: PyQt5 with custom video player widget
- **Video**: OpenCV handles frames, no audio (acceptable for assessment)

### ✅ Testing Complete - Iteration 1 Code

#### Testing Results (2025-11-26)
- ✅ **Automated log analysis completed**
  - Created comprehensive testing checklist (`TESTING_CHECKLIST.md`)
  - All core features verified through application logs:
    - Video loading: 4551 frames, 30fps, 151 seconds ✅
    - Playback controls: Play/Pause/Stop ✅
    - Timeline seeking: Accurate frame navigation ✅
    - Mute toggle: Working correctly ✅
    - Speed control: 1.5x and 2x verified ✅
    - Resource cleanup: Proper shutdown ✅
  - Known limitation documented: OpenCV backend has no audio playback (acceptable for assessment)
  - H.264 codec warnings are normal and don't affect functionality

### 🔄 In Progress - Iteration 1 Completion

#### Remaining Documentation Tasks
1. ✅ ~~Write user scenarios~~ → DONE
2. ✅ ~~Write scoping analysis~~ → DONE
3. ✅ ~~Create testing checklist~~ → DONE
4. 📋 **Write UI/UX theory research document** (`docs/iteration1/theory_research.md`)
   - Document HCI principles applied (Fitts's Law, Hick's Law, Gestalt, etc.)
   - Competitive analysis (VLC, Windows Media Player, etc.)
   - Citations for academic report
5. 📋 **Create ethics documentation templates** (`docs/ethics/`)
   - Informed consent form
   - Participant information sheet
   - Data privacy protocol
   - Anonymization procedures
6. 📋 **Conduct heuristic evaluation** (3-5 participants)
   - Prepare evaluation materials (Nielsen's heuristics checklist)
   - Recruit participants
   - Execute evaluation sessions
   - Document findings in `docs/iteration1/evaluation1_report.md`
7. 📋 **Create iteration video 1** (45s-1m20s)
   - Show design process
   - Demonstrate prototype
   - Explain evaluation approach
   - Add subtitles

### 📅 Next Immediate Tasks (Iteration 1)
1. Complete UI/UX theory research document
2. Prepare ethics templates (before any user testing)
3. Create lo-fi prototype documentation (wireframes/sketches)
4. Recruit heuristic evaluation participants
5. Conduct and document first evaluation

---

## Iteration 2 Status (Updated: 2025-11-26)

### ✅ Completed - All Core Features Implemented

#### Video Editing Features
- ✅ **Video Trimming/Cutting System**
  - In/Out point markers (I and O keys)
  - Visual trim indicators (green In, red Out labels)
  - FFmpeg integration for actual trimming
  - Clear trim points functionality
  - File: `src/video/ffmpeg_processor.py`

- ✅ **Multi-Clip Timeline**
  - Timeline data model (`src/video/timeline.py`)
  - TimelineClip class with position/duration management
  - Add, remove, reorder operations
  - Timeline widget UI (`src/ui/timeline_widget.py`)
  - Clip visualization with thumbnails and durations
  - Drag-and-drop reordering (基础实现)

- ✅ **Marker System for Navigation**
  - Marker data model (`src/video/marker.py`)
  - Add markers at current position (M key)
  - Navigate with [ and ] keys
  - Visual marker indicators (colored flags)
  - Click markers to jump to positions
  - 8 predefined colors with auto-cycling

#### Accessibility Features
- ✅ **High Contrast Mode (WCAG 2.1 AAA)**
  - Theme manager (`src/utils/theme_manager.py`)
  - Toggle with Ctrl+Shift+H
  - Black background (#000000)
  - Yellow/white text (#FFFF00 / #FFFFFF)
  - 19:1 contrast ratio (exceeds 7:1 requirement)
  - 3-4px borders for visibility
  - Bold fonts (11pt)
  - Enhanced focus indicators (cyan borders)
  - Theme preference persistence via QSettings

- ✅ **Comprehensive Keyboard Shortcuts**
  - All features accessible without mouse
  - Trim: I (In), O (Out), Ctrl+T (toggle mode)
  - Markers: M (add), [ (prev), ] (next)
  - Edit: Ctrl+Z (undo), Ctrl+Y (redo)
  - View: Ctrl+Shift+H (high contrast)
  - Export: Ctrl+E

#### Export & Processing
- ✅ **Export Dialog with Quality Presets**
  - Export dialog UI (`src/ui/export_dialog.py`)
  - 3 quality options: High (1080p), Medium (720p), Low (480p)
  - FFmpeg integration with CRF encoding
  - Progress bar with status updates
  - File overwrite confirmation
  - Quality info descriptions

- ✅ **FFmpeg Processor**
  - Trim video segments
  - Concatenate multiple clips
  - Quality presets (CRF 18/23/28)
  - Audio encoding (AAC, 192k/128k/96k)
  - Resolution scaling
  - Background worker thread support

#### Undo/Redo System
- ✅ **Command Pattern Implementation**
  - CommandStack class (`src/utils/command_stack.py`)
  - Supports: Add/Remove clips, Add/Remove markers, Reorder clips
  - Stack limit: 100 commands
  - Ctrl+Z / Ctrl+Y shortcuts
  - Menu integration (Edit > Undo/Redo)
  - Automatic redo stack clearing on new action

#### UI Integration
- ✅ **Enhanced Main Window (Iteration 2)**
  - Main window v2 (`src/ui/main_window_v2.py`)
  - Splitter layout (60% video, 40% timeline)
  - Menu bar with all features:
    - File: Open, Export, Exit
    - Edit: Undo, Redo, Trim Mode, In/Out Points
    - View: Fullscreen, High Contrast
    - Markers: Add, Previous, Next
  - Status bar feedback for all actions
  - Entry point: `src/main_v2.py`

#### Documentation
- ✅ **Iteration 2 Planning Document**
  - Detailed feature breakdown (`docs/iteration2/iteration2_plan.md`)
  - HCI principles mapping
  - Architecture design
  - Implementation timeline
  - Risk management

- ✅ **Testing Documentation**
  - Comprehensive checklist (`docs/iteration2/TESTING_CHECKLIST_ITERATION2.md`)
  - 11 testing categories
  - WCAG compliance checks
  - Performance benchmarks
  - Known limitations documented

- ✅ **Cognitive Walkthrough Guide**
  - Evaluation methodology (`docs/iteration2/cognitive_walkthrough_guide.md`)
  - 3 detailed task scenarios
  - Data collection sheets
  - Analysis framework
  - Ethical considerations

- ✅ **User Guide (README)**
  - Complete feature documentation (`docs/iteration2/README_ITERATION2.md`)
  - Installation instructions
  - Keyboard shortcuts reference
  - Troubleshooting guide
  - HCI principles explanation

### 🔄 Iteration 2 - Remaining Tasks

#### Evaluation & Refinement
1. 📋 **Conduct Cognitive Walkthrough**
   - Recruit 3-5 participants (novice/intermediate/advanced)
   - Execute 3 tasks: Trim video, Combine clips, Use markers
   - Collect metrics: completion rate, time, errors, satisfaction
   - Document in `docs/iteration2/evaluation2_report.md`

2. 📋 **Create Iteration Video 2** (45s-1m20s)
   - Show editing features in action
   - Demonstrate accessibility (high contrast mode)
   - Explain cognitive walkthrough process
   - Add subtitles for accessibility

3. 📋 **Analyze Feedback & Plan Iteration 3**
   - Categorize issues (Critical/High/Medium/Low)
   - Prioritize fixes for Iteration 3
   - Document in `docs/iteration2/feedback_integration.md`

#### Optional Enhancements (Time Permitting)
4. 📋 **FFmpeg Error Handling**
   - Better error messages if FFmpeg missing
   - Installation guide in dialog
   - Graceful fallback for export

5. 📋 **Timeline Playback**
   - Play across multiple clips
   - Visual playhead on timeline
   - Sync video player with timeline position

6. 📋 **Marker Label Editing**
   - Double-click marker to edit label
   - Color picker for custom colors
   - Marker management panel

### Technical Debt & Known Issues

1. **Timeline Playback Not Implemented**
   - UI完整，但播放逻辑待实现
   - 可以导出多片段视频，但不能预览播放
   - 计划在 Iteration 3 或未来完成

2. **Drag-and-Drop Reordering**
   - 基础框架已实现，但拖动反馈可以改进
   - 当前通过 reorder_clip() 方法工作

3. **OpenCV No Audio**
   - 已知限制，已文档化
   - 导出视频包含音频（通过FFmpeg）

4. **FFmpeg Installation Required**
   - 导出功能需要用户手动安装 FFmpeg
   - 应用会检测并提示，但不能自动安装

### Code Statistics (Iteration 2)

**New Files Created**: 10
- `src/video/ffmpeg_processor.py` (300+ lines)
- `src/video/timeline.py` (250+ lines)
- `src/video/marker.py` (200+ lines)
- `src/ui/timeline_widget.py` (350+ lines)
- `src/ui/export_dialog.py` (200+ lines)
- `src/ui/main_window_v2.py` (500+ lines)
- `src/utils/theme_manager.py` (300+ lines)
- `src/utils/command_stack.py` (250+ lines)
- `src/main_v2.py` (30 lines)

**Documentation**: 3 comprehensive guides (8000+ words total)

**Total Lines of Code (Iteration 1+2)**: ~3,000 lines

## Key Contacts & Resources

- **Module Leader**: Samson Fabiyi
- **Staff Contact**: Danyang Zheng
- **Repository**: https://github.com/Mikuu177/qt-cw-vedio
- **Assessment Brief**: See `XJCO2811_Assessment Brief_25-26.pdf` in parent directory

## References to Keep Handy

- Nielsen's 10 Usability Heuristics
- WCAG 2.1 Guidelines (Level AA)
- SUS (System Usability Scale) calculation method
- Qt Documentation (especially QMediaPlayer, QTranslator)
- FFmpeg command-line reference for video editing
