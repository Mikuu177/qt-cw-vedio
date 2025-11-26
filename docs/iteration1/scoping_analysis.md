# Scoping Analysis - Video Editor/Player

## Executive Summary

This document defines the scope, priorities, and boundaries for the video editor/player project. Using the MoSCoW prioritization method, we identify essential features for each iteration while maintaining focus on the assessment requirements and user scenarios.

**Project Goal**: Develop a functional video editor/player that demonstrates UI/UX principles through iterative design and evaluation.

**Time Constraint**: 4 weeks (3 iterations + final submission)

---

## Analysis of Tomeo Application

### Current Tomeo Features
The Tomeo application (base framework) provides:
- Basic video playback using Qt's QMediaPlayer
- Simple play/pause controls
- Minimal UI layout

### Limitations Identified
1. **Codec Support**: QMediaPlayer has limited codec support on Windows
2. **No Editing**: Only playback, no video editing capabilities
3. **Limited Accessibility**: No keyboard shortcuts or accessibility features
4. **No Multi-clip Support**: Cannot work with multiple video files
5. **Basic UI**: Minimal interface, no timeline visualization
6. **No Internationalization**: English only
7. **No Error Handling**: Poor user feedback on errors

### Improvement Opportunities
Based on user scenarios and Tomeo limitations:

1. **Enhanced Playback** ✓
   - Better codec support (OpenCV backend)
   - Visual timeline with time display
   - Smooth seeking and navigation

2. **Video Editing** (Iteration 2+)
   - Trim/cut functionality
   - Multi-clip timeline assembly
   - Marker system for navigation

3. **Accessibility** (All iterations)
   - Comprehensive keyboard shortcuts
   - High contrast mode
   - Screen reader compatibility

4. **User Experience**
   - Clear visual feedback
   - Intuitive controls
   - Error prevention and recovery

---

## Feature Prioritization: MoSCoW Analysis

### Iteration 1: Foundation

#### MUST HAVE (Critical for Iteration 1)
- ✅ **Video playback** with play/pause/stop controls
- ✅ **Timeline slider** for video seeking
- ✅ **Time display** showing current and total time
- ✅ **File opening** via menu or dialog
- ✅ **Keyboard shortcuts** for basic accessibility
  - Space: Play/Pause
  - Left/Right: Seek backward/forward
  - Ctrl+O: Open file
- ✅ **Error handling** with user-friendly messages
- ✅ **Status bar** for system feedback

**Rationale**: These features enable basic video playback and satisfy Nielsen's heuristics for Iteration 1 evaluation.

#### SHOULD HAVE (Important but not critical)
- ⏳ Volume control with visual indicator
- ⏳ Responsive window resizing
- ⏳ Auto-load sample video for demonstration
- ⏳ Application icon and branding

**Rationale**: Enhance usability but project is viable without them.

#### COULD HAVE (Nice to have)
- 📋 Playlist support
- 📋 Recent files menu
- 📋 Playback speed control (0.5x, 1x, 1.5x, 2x)

**Rationale**: Add value but low priority for assessment criteria.

#### WON'T HAVE (Out of scope for Iteration 1)
- ❌ Video editing (trim/cut) → Iteration 2
- ❌ Multi-clip timeline → Iteration 2
- ❌ Filters/effects → Iteration 2/3
- ❌ Export functionality → Iteration 3
- ❌ Internationalization → Iteration 3
- ❌ Social features (likes, comments, sharing)

---

### Iteration 2: Enhancement

#### MUST HAVE
- **Video trimming/cutting**
  - Mark in/out points on timeline
  - Preview trimmed result
  - FFmpeg integration for processing

- **Multi-clip timeline**
  - Add multiple clips to project
  - Arrange clips in sequence
  - Visual representation of all clips

- **Enhanced accessibility**
  - High contrast mode toggle
  - Extended keyboard shortcuts
  - Improved screen reader support

- **Marker system**
  - Add/remove markers on timeline
  - Jump to markers
  - Marker labels/descriptions

#### SHOULD HAVE
- Basic video filters (brightness, contrast, saturation)
- Drag-and-drop file opening
- Timeline zoom controls

#### COULD HAVE
- Video transitions between clips
- Audio level adjustment
- Subtitle display support

#### WON'T HAVE
- Advanced effects (chroma key, motion tracking)
- Audio editing beyond volume
- 3D video support

---

### Iteration 3: Refinement

#### MUST HAVE
- **Internationalization**
  - English/Chinese language support
  - Language switching in settings
  - All UI text translatable

- **Export functionality**
  - Export edited video to MP4
  - Quality/resolution options
  - Progress indicator

- **Undo/Redo system**
  - Command pattern implementation
  - Support for all editing operations
  - Clear visual indication of state

- **Performance optimization**
  - Smooth playback (30+ FPS)
  - Responsive UI (no freezing)
  - Efficient memory usage

#### SHOULD HAVE
- Export presets (YouTube, Email, etc.)
- Thumbnail preview on timeline
- Auto-save project state

#### COULD HAVE
- Batch export multiple projects
- Custom export profiles
- GPU acceleration

#### WON'T HAVE
- Cloud storage integration
- Online collaboration features
- Mobile app version

---

## Technical Feasibility Assessment

### Technology Stack

#### Frontend: PyQt5 ✓
**Pros**:
- Cross-platform (Windows primary target)
- Rich widget library
- Good documentation
- Python = rapid development

**Cons**:
- Performance overhead vs C++
- Larger distribution size

**Decision**: ✅ Use PyQt5 - advantages outweigh disadvantages for 4-week timeline

#### Video Backend: OpenCV ✓
**Pros**:
- Excellent codec support
- Cross-platform
- Easy frame manipulation (for editing)
- No licensing issues

**Cons**:
- No audio playback
- Requires frame-by-frame rendering

**Decision**: ✅ Use OpenCV - codec support critical, audio can be added later if needed

#### Video Editing: FFmpeg (Iteration 2+)
**Pros**:
- Industry standard
- Comprehensive format support
- Command-line interface

**Cons**:
- External dependency
- Learning curve

**Decision**: ✅ Use FFmpeg - necessary for professional editing features

#### Data Storage: SQLite (Iteration 2+)
**Pros**:
- Lightweight
- No server required
- Built into Python

**Cons**:
- Single-user only
- Limited for large datasets

**Decision**: ✅ Use SQLite - sufficient for user preferences and project state

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| FFmpeg integration complexity | Medium | High | Allocate full week in Iteration 2, use python wrapper |
| Codec support issues | Low | Medium | Already mitigated with OpenCV |
| Performance problems | Medium | Medium | Early testing, optimization sprint in Iteration 3 |
| User recruitment delays | Medium | High | Start recruitment early, over-recruit participants |
| Time overrun | Medium | Critical | Strict scope adherence, cut "COULD HAVE" features first |
| Audio playback missing | High | Medium | Document as known limitation, focus on video |

---

## Resource Planning

### Development Time Allocation

**Iteration 1** (Week 1-2): 40-50 hours
- Code: 20 hours (basic playback implemented ✓)
- Documentation: 10 hours (scenarios, analysis, theory)
- Evaluation: 10 hours (heuristic evaluation)
- Video production: 5 hours (iteration video 1)

**Iteration 2** (Week 2-3): 40-50 hours
- Code: 25 hours (editing features, FFmpeg integration)
- Documentation: 5 hours (feedback integration)
- Evaluation: 12 hours (cognitive walkthrough)
- Video production: 5 hours (iteration video 2)

**Iteration 3** (Week 3-4): 40-50 hours
- Code: 20 hours (i18n, export, undo/redo)
- Optimization: 8 hours (performance tuning)
- Evaluation: 12 hours (SUS questionnaire + analysis)
- Video production: 5 hours (iteration video 3)

**Final Submission** (Week 4): 20-30 hours
- Report writing: 15 hours (6 pages + references)
- Showcase video: 5 hours (1-1.5 minutes)
- Code documentation: 5 hours (README, comments)
- Package preparation: 3 hours

**Total**: 160-180 hours over 4 weeks

### Tools and Resources Required

**Development**:
- Python 3.8+
- PyQt5, OpenCV
- FFmpeg
- Git/GitHub

**Design**:
- Figma or Adobe XD (for prototypes)
- Screenshot tools
- Screen recording software

**Evaluation**:
- Nielsen's 10 heuristics checklist
- Cognitive walkthrough template
- SUS questionnaire (standard 10 questions)
- 10-15 evaluation participants across 3 iterations

**Documentation**:
- Markdown editor
- LaTeX or Word (for final report)
- Video editing for demo videos
- Subtitle creation tools

---

## Success Criteria by Iteration

### Iteration 1
✅ **Code**: Video plays smoothly with all basic controls working
✅ **Stability**: No crashes during normal operation
✅ **Accessibility**: All functions accessible via keyboard
📋 **Documentation**: Scenarios, scoping, theory research complete
📋 **Evaluation**: Heuristic evaluation with 3-5 participants
📋 **Video**: 45s-1m20s iteration video showing process

### Iteration 2
- **Code**: Can trim videos and combine clips
- **Usability**: Editing workflow is learnable without tutorial
- **Accessibility**: High contrast mode functional
- **Documentation**: Feedback integration document
- **Evaluation**: Cognitive walkthrough with 3-5 participants
- **Video**: 45s-1m20s iteration video showing improvements

### Iteration 3
- **Code**: Can export edited videos with i18n support
- **Performance**: 30+ FPS playback, responsive UI
- **Quality**: SUS score >68 (above average)
- **Documentation**: All iteration reports complete
- **Evaluation**: SUS questionnaire with 5-10 participants
- **Video**: 45s-1m20s final iteration video

### Final Submission
- **Report**: 6-page academic report linking theory to practice
- **Showcase**: 1-1.5 minute professional demo video
- **Code**: Well-documented, stable, complete
- **Package**: All deliverables organized in submission folder

---

## Scope Boundaries (What We're NOT Building)

To maintain focus and meet deadlines, the following are explicitly out of scope:

### Not a Social Media Platform
- ❌ User profiles and accounts
- ❌ Social features (likes, comments, sharing)
- ❌ Online collaboration
- ❌ Cloud storage/streaming

### Not Professional Video Editor
- ❌ Advanced color grading
- ❌ Motion graphics
- ❌ 3D effects
- ❌ Multi-camera editing
- ❌ Advanced audio mixing

### Not Media Management System
- ❌ Video library/database
- ❌ Metadata tagging
- ❌ Face recognition
- ❌ Automatic categorization

**Focus**: Simple, accessible video playback and editing for educational/personal use

---

## Conclusion

This scoping analysis provides clear boundaries and priorities for the project:

1. **Iteration 1** focuses on solid playback foundation (✓ Complete)
2. **Iteration 2** adds core editing features
3. **Iteration 3** polishes and optimizes

The MoSCoW prioritization ensures we deliver essential features while maintaining flexibility to cut non-critical items if time constraints arise.

**Next Steps**:
1. Complete Iteration 1 documentation (theory research, ethics)
2. Conduct heuristic evaluation with participants
3. Produce iteration video 1
4. Begin planning Iteration 2 features

---

*Document created: 2025-11-26*
*For: XJCO2811 User Interfaces Assessment - Iteration 1*
