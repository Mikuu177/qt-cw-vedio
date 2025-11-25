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

## Current Project Status

- ✅ Repository created and structure initialized
- ✅ Project plan documented (34 issues across 4 milestones)
- 🔄 Ready to begin Iteration 1 implementation

### Next Immediate Tasks
1. Write 3 detailed user scenarios in `/docs/iteration1/scenarios.md`
2. Research and document UI/UX theory in `/docs/iteration1/theory_research.md`
3. Create lo-fi prototypes (paper/Figma) in `/prototypes/iteration1/`
4. Set up Qt project and implement basic video playback
5. Prepare ethics documents before first evaluation

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
