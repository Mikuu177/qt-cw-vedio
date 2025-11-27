# Cognitive Walkthrough Evaluation Guide - Iteration 2

## Overview

**Evaluation Method**: Cognitive Walkthrough
**Iteration**: 2
**Date**: 2025-11-26
**Evaluator Instructions**: This document guides evaluators through task-based usability testing

---

## What is Cognitive Walkthrough?

Cognitive Walkthrough is a usability inspection method that focuses on evaluating a system's learnability, particularly for first-time or infrequent users. Evaluators step through specific tasks from a user's perspective, answering key questions at each step.

### Key Questions for Each Step:
1. **Will users know what to do?** - Is the correct action obvious?
2. **Can users see how to do it?** - Are the controls visible and understandable?
3. **Will users understand feedback?** - Is the system response clear?
4. **Will users know they made progress?** - Can they tell they're moving toward their goal?

---

## Participant Profile

### Target Users
- **Novice**: Never used video editing software (e.g., students, teachers)
- **Intermediate**: Used basic editors (Windows Photos, iMovie)
- **Advanced**: Familiar with professional tools (Premiere Pro, Final Cut)

### Recruitment Criteria
- Age: 18-65
- Mix of experience levels (1-2 novice, 2-3 intermediate, 1 advanced)
- No prior exposure to this specific application
- Comfortable using computers

---

## Evaluation Setup

### Materials Needed
- [ ] Computer with application installed
- [ ] Sample video files (provided in `/videos/` folder)
- [ ] Consent form (signed before evaluation)
- [ ] Evaluation recording sheet (one per participant)
- [ ] Timer/stopwatch
- [ ] Screen recording software (optional but recommended)

### Environment
- Quiet room with minimal distractions
- Single participant + 1-2 evaluators
- Duration: 30-45 minutes per session

### Introduction Script

> "Thank you for participating in this usability evaluation. We're testing a video editing application designed for teachers, students, and casual users.
>
> You'll be asked to complete 3 tasks. Please think aloud as you work - tell us what you're thinking, what you're looking for, and any confusion you experience.
>
> Remember: We're testing the software, not you. There are no wrong answers. If you get stuck, that's valuable feedback about the design.
>
> Do you have any questions before we start?"

---

## Task 1: Trim a Video Clip

### Scenario
**User**: Dr. Sarah Chen (University Teacher)
**Goal**: Remove the first 15 seconds of a lecture recording (camera adjustment period)

### Task Description
> "You've recorded a 5-minute lecture, but the first 15 seconds show you adjusting the camera. Please use this application to remove that unwanted section and keep the rest of the video."

### Expected Steps

| Step | Action | CW Questions | Success Criteria |
|------|--------|--------------|------------------|
| **1** | Open the application | Q1: Know what to do? Q2: See File menu? | Application launches |
| **2** | Click "File" > "Open Video" OR Ctrl+O | Q1: Menu option obvious? Q3: File dialog appears? | File dialog opens |
| **3** | Select `lecture_recording.mp4` from test files | Q2: File selector familiar? | Video loads |
| **4** | Play video to find the 15-second mark | Q1: Know to use Play button? Q2: Play button visible? | Video plays |
| **5** | Pause at ~15 seconds | Q2: Pause button clear? | Video paused |
| **6** | Press **I** key to set In point | Q1: Know about I key? Q2: See menu hint? | In point label shows "In: 00:15" |
| **7** | Seek to end of video OR continue playing | Q1: Understand trim concept? | At end of video |
| **8** | Press **O** key to set Out point | Q2: Remember pattern from In point? | Out point label shows |
| **9** | File > Export Video (Ctrl+E) | Q1: Know next step is export? | Export dialog opens |
| **10** | Click "Browse" and choose output path | Q2: Browse button visible? | File path set |
| **11** | Select quality (default High is OK) | Q3: Quality options clear? | Quality selected |
| **12** | Click "Export" | Q4: Export button obvious? | Export starts |
| **13** | Wait for completion | Q3: Progress visible? | Success message |

### Observation Points
- **Discoverability**: Did user find the I/O keys without help?
- **Feedback**: Did user notice In/Out point labels?
- **Error Recovery**: If user set points in wrong order, could they fix it?
- **Learnability**: Did user understand the trim concept?

### Time Expectation
- **Novice**: 4-6 minutes
- **Intermediate**: 3-4 minutes
- **Advanced**: 2-3 minutes

### Common Issues to Watch For
- [ ] User doesn't know about I/O keyboard shortcuts
- [ ] User expects visual trim range on timeline (not implemented)
- [ ] User confused about In/Out point order
- [ ] User doesn't understand what "In point" means
- [ ] User exports full video instead of trimmed version

### Evaluation Questions (Post-Task)
1. "How easy or difficult was that task?" (1-5 scale: 1=Very Difficult, 5=Very Easy)
2. "What was the most confusing part?"
3. "If you had to do this again, would it be easier?"
4. "What would make this task clearer?"

---

## Task 2: Combine Multiple Video Clips

### Scenario
**User**: Alex Martinez (University Student)
**Goal**: Create a presentation by combining 3 short video clips in sequence

### Task Description
> "You've created 3 separate video clips for a presentation: an introduction, main content, and conclusion. Please combine them into a single video in the correct order."

### Expected Steps

| Step | Action | CW Questions | Success Criteria |
|------|--------|--------------|------------------|
| **1** | Look for timeline area at bottom | Q2: Timeline widget visible? | User notices timeline section |
| **2** | Click "+ Add Clip" button | Q1: Button purpose clear? | File dialog opens |
| **3** | Select `intro.mp4` | Q2: File dialog standard? | Clip added to timeline |
| **4** | Observe clip appears in timeline | Q3: Visual feedback clear? | Clip widget shows with duration |
| **5** | Click "+ Add Clip" again | Q4: Know can add more? | File dialog opens |
| **6** | Select `main_content.mp4` | - | Second clip added |
| **7** | Click "+ Add Clip" again | - | File dialog opens |
| **8** | Select `conclusion.mp4` | - | Third clip added |
| **9** | Check clip order (should be 1-2-3) | Q1: Know how to verify order? | Clips in timeline left-to-right |
| **10** | (Optional) Drag to reorder if needed | Q2: Drag affordance visible? | Clips reordered |
| **11** | File > Export Video | Q1: Know next step? | Export dialog opens |
| **12** | Select output path | - | Path set |
| **13** | Click Export | - | Multi-clip export starts |

### Observation Points
- **Mental Model**: Does user understand timeline left-to-right = chronological order?
- **Drag-and-Drop**: Can user discover reordering by dragging?
- **Feedback**: Does timeline info ("3 clips | Total duration: XX.Xs") help?
- **Visibility**: Is the "+ Add Clip" button prominent enough?

### Time Expectation
- **Novice**: 5-7 minutes
- **Intermediate**: 3-5 minutes
- **Advanced**: 2-3 minutes

### Common Issues to Watch For
- [ ] User doesn't see timeline widget (below fold?)
- [ ] User adds all clips but doesn't know how to export
- [ ] User confused about clip order (expects playback to show)
- [ ] User tries to preview combined timeline (not implemented)
- [ ] User deletes clip by accident and doesn't know about undo

### Evaluation Questions (Post-Task)
1. "Did the timeline concept make sense to you?"
2. "How would you expect to preview the combined video before exporting?"
3. "Was the clip order clear visually?"
4. "What confused you, if anything?"

---

## Task 3: Mark Important Moments for Navigation

### Scenario
**User**: Robert Williams (Amateur Video Editor)
**Goal**: Mark 3 key moments in a 10-minute video for easy navigation during editing

### Task Description
> "You have a 10-minute video and need to find 3 specific moments: the introduction (0:30), main topic (5:00), and conclusion (9:00). Use markers to mark these moments so you can quickly jump between them."

### Expected Steps

| Step | Action | CW Questions | Success Criteria |
|------|--------|--------------|------------------|
| **1** | Open `long_video.mp4` | - | Video loads |
| **2** | Play and seek to 0:30 | Q2: Seek using slider? | At 0:30 mark |
| **3** | Press **M** key to add marker | Q1: Discover M key how? | Marker added, appears in marker bar |
| **4** | Notice marker appears (colored flag) | Q3: Visual feedback clear? | Marker visible |
| **5** | Seek to 5:00 | - | At 5:00 mark |
| **6** | Press **M** again | Q4: Remember pattern from step 3? | Second marker added |
| **7** | Seek to 9:00 | - | At 9:00 mark |
| **8** | Press **M** again | - | Third marker added |
| **9** | Click on first marker | Q1: Know markers are clickable? | Video jumps to 0:30 |
| **10** | Press **]** key to go to next marker | Q1: Discover bracket keys how? | Video jumps to 5:00 |
| **11** | Press **]** again | - | Video jumps to 9:00 |
| **12** | Press **[** to go back | Q2: Infer [ is opposite of ]? | Video jumps to 5:00 |

### Observation Points
- **Discoverability**: How do users find marker feature? (Menu hint vs. keyboard)
- **Affordance**: Do users understand markers are clickable?
- **Navigation**: Do users discover [ and ] keys or rely on clicking?
- **Visual Design**: Are marker colors/shapes distinctive enough?

### Time Expectation
- **Novice**: 6-8 minutes
- **Intermediate**: 4-5 minutes
- **Advanced**: 3-4 minutes

### Common Issues to Watch For
- [ ] User doesn't discover M key (looks for button instead)
- [ ] User adds marker but doesn't know how to jump to it
- [ ] User doesn't understand marker bar visualization
- [ ] User confused by automatic marker colors
- [ ] User wants to label markers (feature not implemented in UI yet)

### Evaluation Questions (Post-Task)
1. "How did you discover the marker feature?"
2. "Was the marker visualization helpful?"
3. "Would you use markers in your own videos? Why or why not?"
4. "What would make markers more useful?"

---

## Additional Evaluation Dimensions

### Accessibility Testing (High Contrast Mode)

**Task**: Enable high contrast mode and repeat one task

1. Go to View > High Contrast Mode (or Ctrl+Shift+H)
2. Verify theme changes to black background, yellow text
3. Attempt to complete Task 1 (trim video) in high contrast mode
4. Evaluate:
   - [ ] Is all text readable? (WCAG 7:1 contrast ratio)
   - [ ] Are button borders visible?
   - [ ] Are focus indicators clear?
   - [ ] Is it easier or harder to use?

**Post-Test Question**: "Would you use high contrast mode regularly? In what situations?"

---

### Undo/Redo Testing

**Task**: Test error recovery

1. Add 3 clips to timeline
2. Delete the middle clip
3. Press Ctrl+Z (undo) - clip should reappear
4. Press Ctrl+Y (redo) - clip should disappear again
5. Add a new clip (redo stack should clear)

**Evaluation**:
- [ ] Did user understand undo/redo immediately?
- [ ] Was visual feedback sufficient?
- [ ] Did user know undo was available?

---

## Data Collection Sheet

### Participant Information
- **Participant ID**: P-[number] (anonymized)
- **Experience Level**: [ ] Novice [ ] Intermediate [ ] Advanced
- **Age Range**: [ ] 18-25 [ ] 26-35 [ ] 36-50 [ ] 51-65
- **Prior Video Editing**: [ ] None [ ] Basic [ ] Professional

### Task Completion Matrix

| Task | Completed? | Time (min) | Errors | Help Needed? | Satisfaction (1-5) |
|------|-----------|-----------|--------|--------------|-------------------|
| 1. Trim Video | ☐ Yes ☐ No | ___ | ___ | ☐ Yes ☐ No | ☐1 ☐2 ☐3 ☐4 ☐5 |
| 2. Combine Clips | ☐ Yes ☐ No | ___ | ___ | ☐ Yes ☐ No | ☐1 ☐2 ☐3 ☐4 ☐5 |
| 3. Markers | ☐ Yes ☐ No | ___ | ___ | ☐ Yes ☐ No | ☐1 ☐2 ☐3 ☐4 ☐5 |

### Error Tracking

| Step | Error Description | Recovery Method | Severity (Low/Med/High) |
|------|------------------|-----------------|------------------------|
| ___ | ___ | ___ | ___ |

### Quotes & Observations

**Positive Comments**:
-
-

**Negative Comments / Confusion**:
-
-

**Suggestions**:
-
-

---

## Post-Evaluation Interview Questions

### General Usability
1. "Overall, how intuitive was this application?" (1-5 scale)
2. "Which feature was easiest to learn?"
3. "Which feature was most confusing?"
4. "Did you feel in control throughout the tasks?"

### Feature-Specific
5. "How useful is the marker system for your needs?"
6. "Would you prefer visual trim handles on the timeline instead of I/O keys?"
7. "Is high contrast mode necessary for you? Why or why not?"
8. "What features are missing that you expected?"

### Comparison (if applicable)
9. "Compared to other video editors you've used, how does this rank?"
10. "Would you use this for your video editing tasks?"

---

## Analysis Framework

### Metrics to Calculate
- **Task Success Rate**: % of participants who completed each task without assistance
- **Average Time on Task**: Mean time for successful completions
- **Error Rate**: Average errors per task
- **Satisfaction Score**: Mean rating (1-5 scale)

### Issues Categorization
- **Critical**: Prevents task completion (fix in Iteration 3)
- **High**: Causes significant frustration (fix if time permits)
- **Medium**: Minor confusion, users recover (consider for future)
- **Low**: Cosmetic or preference-based (note for polish)

### Example Analysis Table

| Issue | Frequency (N/5) | Severity | Proposed Solution |
|-------|----------------|----------|-------------------|
| Users don't discover I/O keys | 4/5 | High | Add visual hint on timeline or button |
| Marker colors not customizable | 2/5 | Low | Allow color picker in future |
| No visual trim range | 5/5 | Critical | Implement timeline trim overlay |

---

## Iteration 3 Planning

Based on cognitive walkthrough results, prioritize improvements for Iteration 3:

1. **Address Critical Issues**: Features that blocked task completion
2. **Improve Learnability**: Add hints, tooltips, or onboarding
3. **Enhance Feedback**: Clearer visual/audio cues
4. **Polish Accessibility**: Refine high contrast mode based on feedback

Document all findings in `/docs/iteration2/evaluation2_report.md`

---

## Ethical Considerations

- [ ] Informed consent obtained before session
- [ ] Participant understands they can stop anytime
- [ ] Data will be anonymized (no names in reports)
- [ ] Screen recordings deleted after analysis (if recorded)
- [ ] Participants offered opportunity to ask questions

---

## References

- Wharton, C., Rieman, J., Lewis, C., & Polson, P. (1994). The cognitive walkthrough method: A practitioner's guide.
- Nielsen, J. (1994). Usability inspection methods. CHI '94 Conference Companion.
- ISO 9241-11: Usability - Definitions and concepts

---

*Document Version: 1.0*
*Last Updated: 2025-11-26*
*For: XJCO2811 User Interfaces - Iteration 2 Evaluation*
