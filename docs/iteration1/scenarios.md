# User Scenarios - Iteration 1

## Overview
This document presents three detailed user scenarios that guide the design and development of the video editor/player application. These scenarios represent the primary target users and their needs.

---

## Scenario 1: Teacher Editing Educational Videos

### User Profile
- **Name**: Dr. Sarah Chen (anonymized)
- **Role**: University Lecturer in Computer Science
- **Age**: 35-45
- **Technical Proficiency**: Intermediate
- **Context**: Teaches online and hybrid courses

### Current Situation
Dr. Chen records lectures using screen capture software and needs to edit them before uploading to the university's learning management system. She needs to:
- Remove mistakes and pauses from recordings
- Trim unnecessary content from the beginning and end
- Add markers to highlight important sections
- Ensure videos are accessible to all students

### Pain Points with Current Tools
- Adobe Premiere is too complex and expensive for basic editing
- Free tools like VLC don't support editing
- Windows Movie Maker is discontinued
- Needs quick, simple editing without steep learning curve

### Goals
- **Primary**: Quickly trim and clean up lecture recordings
- **Secondary**: Make videos accessible (subtitles, keyboard navigation)
- **Time Constraint**: Should take less than 10 minutes to edit a 1-hour lecture

### Scenario Narrative
Dr. Chen finishes recording a 65-minute lecture on database design. The first 3 minutes contain setup time and technical issues. She wants to:

1. **Open the video** quickly without navigating complex menus
2. **Preview the content** to identify what needs trimming
3. **Mark the start point** at 3:15 where the actual lecture begins
4. **Trim the beginning** to remove setup time
5. **Add markers** at key concept transitions for student navigation
6. **Preview the result** to ensure smooth transitions
7. **Export the edited video** in a format compatible with the LMS

### Success Criteria
- Can complete basic edits in under 5 minutes
- No need to read documentation or watch tutorials
- All functions accessible via keyboard (for accessibility demonstrations)
- Output file compatible with university systems

### Design Implications
- **Fitts's Law**: Large, easily clickable trim controls
- **Visibility**: Clear visual feedback of trim points on timeline
- **Error Prevention**: Undo capability for accidental edits
- **Efficiency**: Keyboard shortcuts for common operations
- **Accessibility**: Screen reader compatible for teaching accessibility

---

## Scenario 2: Student Creating Project Presentations

### User Profile
- **Name**: Alex Martinez (anonymized)
- **Role**: Final-year Computer Science Student
- **Age**: 20-25
- **Technical Proficiency**: Advanced
- **Context**: Working on coursework video presentation

### Current Situation
Alex needs to create a 5-minute video presentation combining:
- Screen recordings of software demonstrations
- Webcam footage explaining concepts
- Multiple short clips that need to be assembled
- Clear transitions between sections

### Pain Points with Current Tools
- iMovie not available on Windows
- DaVinci Resolve too complex for quick projects
- Online tools require good internet connection (not reliable in dorm)
- Need simple multi-clip assembly without advanced features

### Goals
- **Primary**: Combine multiple video clips into one presentation
- **Secondary**: Trim individual clips and arrange them logically
- **Quality**: Maintain original video quality
- **Time Constraint**: Complete editing in one evening

### Scenario Narrative
Alex has recorded:
- 3 screen capture clips (2-3 minutes each) showing code demonstrations
- 2 webcam clips (1-2 minutes each) explaining concepts
- Need to create a cohesive 5-minute presentation by:

1. **Import multiple clips** into the application
2. **Trim each clip** to remove errors and unnecessary parts
3. **Arrange clips on timeline** in logical order
4. **Preview the complete sequence** to check flow
5. **Adjust timing** if needed
6. **Export final video** for submission

### Success Criteria
- Can assemble 5 clips in under 15 minutes
- Clear visual representation of multi-clip timeline
- Easy to rearrange clip order
- No quality loss in exported video
- Works offline without internet dependency

### Design Implications
- **Gestalt Principles**: Visual grouping of clips on timeline
- **Drag-and-drop**: Intuitive clip arrangement
- **Visual Feedback**: Clear indication of clip boundaries and order
- **Direct Manipulation**: Easy to grab and move timeline elements
- **Consistency**: Standard video editing conventions (left-to-right timeline)

---

## Scenario 3: Amateur Editing Personal Videos

### User Profile
- **Name**: Robert Williams (anonymized)
- **Role**: Amateur Videographer / Hobbyist
- **Age**: 45-55
- **Technical Proficiency**: Basic to Intermediate
- **Context**: Edits family videos and travel footage

### Current Situation
Robert enjoys recording family events and travel experiences but finds most editing software overwhelming. He needs simple tools to:
- Remove shaky or unwanted footage
- Combine best moments into highlight videos
- Share with family via email or USB drive
- Preserve memories in organized, watchable format

### Pain Points with Current Tools
- Professional tools (Adobe, Final Cut) too expensive and complex
- Smartphone apps limited by small screen
- Many tools require subscription (not willing to pay monthly)
- Just wants simple, one-time tool for occasional use

### Goals
- **Primary**: Create watchable highlight videos from raw footage
- **Secondary**: Simple trimming and basic quality adjustments
- **Ease of Use**: Should be intuitive without training
- **Cost**: Free or one-time purchase, no subscriptions

### Scenario Narrative
Robert returns from a weekend trip with 45 minutes of video footage. He wants to create a 10-minute highlight video to share with family:

1. **Open the raw footage** from camera SD card
2. **Scan through video** to identify best moments
3. **Add markers** to flag interesting sections
4. **Trim unwanted sections** (shaky footage, ground shots, etc.)
5. **Apply basic improvements** if possible (brightness, stability)
6. **Preview the result** on full screen
7. **Export in common format** (MP4) for easy sharing

### Success Criteria
- Can identify and mark good sections while watching through once
- Trimming feels natural and reversible
- Preview shows exactly what will be exported
- Exported file size reasonable for email/USB sharing
- No confusing technical jargon in interface

### Design Implications
- **Simplicity**: Hide advanced features, show only essentials
- **Feedback**: Constant visual preview of edits
- **Error Recovery**: Easy undo for mistakes
- **Hick's Law**: Limited menu choices to reduce decision time
- **Plain Language**: No technical terminology in labels
- **Visibility of System Status**: Clear indication of what's happening

---

## Cross-Scenario Requirements

### Common Needs
All three scenarios require:

1. **Reliable Video Playback**
   - Smooth, responsive playback
   - Accurate seeking and timeline navigation
   - Clear time display (current/total)

2. **Intuitive Timeline Interface**
   - Visual representation of video duration
   - Easy to understand position indicator
   - Responsive to mouse and keyboard input

3. **Basic Editing Capabilities**
   - Trim/cut functionality
   - Marker/annotation system
   - Undo/redo support

4. **Accessibility**
   - Keyboard shortcuts for all major functions
   - High contrast mode for visibility
   - Clear, readable text and labels

5. **File Management**
   - Easy file opening (drag-drop or file dialog)
   - Common format support (MP4, AVI, MOV)
   - Export to standard formats

### Unique Requirements

**Dr. Chen (Teacher)**:
- Accessibility features for teaching examples
- Quick editing workflow
- Professional output quality

**Alex (Student)**:
- Multi-clip support
- Offline functionality
- Fast learning curve

**Robert (Amateur)**:
- Maximum simplicity
- Forgiving interface (easy to undo)
- No subscription costs

---

## Design Priorities Based on Scenarios

### Iteration 1 Focus
1. **Reliable playback** (all scenarios)
2. **Simple, clear interface** (Robert's priority)
3. **Keyboard accessibility** (Dr. Chen's priority)
4. **Timeline navigation** (all scenarios)

### Iteration 2 Focus
1. **Trim/cut editing** (all scenarios)
2. **Multi-clip timeline** (Alex's priority)
3. **Marker system** (Dr. Chen and Robert)
4. **Enhanced accessibility** (Dr. Chen's priority)

### Iteration 3 Focus
1. **Export functionality** (all scenarios)
2. **Internationalization** (broader accessibility)
3. **Performance optimization** (all scenarios)
4. **Final polish** (all scenarios)

---

## Evaluation Connection

These scenarios will guide:
- **Iteration 1 Heuristic Evaluation**: Test against usability principles for basic playback
- **Iteration 2 Cognitive Walkthrough**: Task-based testing of editing workflow
- **Iteration 3 SUS Questionnaire**: Overall usability assessment with representative users

Each scenario represents real user needs that can be tested and validated through the evaluation cycles.

---

*Document created: 2025-11-26*
*For: XJCO2811 User Interfaces Assessment - Iteration 1*
