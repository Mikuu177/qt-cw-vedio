# Video Editor/Player - XJCO2811 User Interfaces Assessment

## Project Overview
An enhanced video editor and player application based on the Tomeo application, developed as part of the XJCO2811 User Interfaces module at the University of Leeds.

## Project Goals
- Design and implement a functional video editor/player with advanced features
- Apply UI/UX principles and interaction design lifecycle
- Conduct iterative development with user evaluation
- Create accessible and internationalized interface

## Key Features (Planned)

### Video Playback
- Basic controls: play, pause, fast-forward, rewind, seek
- Variable playback speed (0.5x, 1x, 1.5x, 2x)
- Volume control, mute, and fullscreen mode
- Timeline view with thumbnail preview

### Video Editing
- Trim and cut video clips
- Multi-clip assembly
- Marker points for navigation
- Simple filters and effects
- Export edited videos

### User Interface
- Responsive design for different window sizes
- Accessibility features:
  - Keyboard shortcuts
  - Screen reader support
  - High contrast mode
  - Subtitle display
- Internationalization (English/Chinese)
- Undo/redo functionality

## Technology Stack
- **Framework**: PyQt5 (Python Qt bindings)
- **Video Processing**: QMediaPlayer (playback), FFmpeg (editing - Iteration 2+)
- **Data Storage**: SQLite (for user preferences and project history - Iteration 2+)
- **UI Design**: Figma/Adobe XD (prototyping)

## Project Timeline

### Iteration 1 (Weeks 1-2)
- Requirement analysis and scenario design
- Lo-fi prototypes
- UI/UX theory research
- First evaluation cycle
- Ethics documentation

### Iteration 2 (Weeks 2-3)
- Hi-fi prototype development
- Core playback features implementation
- Second evaluation cycle
- Accessibility implementation

### Iteration 3 (Weeks 3-4)
- Video editing features
- Internationalization
- Third evaluation cycle
- Performance optimization

### Final Submission (Week 4)
- Documentation and report
- Video demonstrations
- Code cleanup and submission

## Assessment Components
- **Prototype** (20%): Stable, functional application with creative improvements
- **Report** (30%): 6-page documentation covering theory, method, and results
- **Videos** (20%): 3 iteration videos + 1 showcase video
- **Experiments/Iterations** (20%): Three complete evaluation cycles
- **Module Participation** (10%): Peer feedback and engagement

## Team Information
- **Module**: XJCO2811 User Interfaces
- **Submission Deadline**: 04/12/2025 10:00 PM (China time)
- **Repository**: https://github.com/Mikuu177/qt-cw-vedio

## Development Guidelines
- Follow HCI principles taught in the module
- Maintain code quality and documentation
- Conduct regular evaluations with real users
- Ensure ethics compliance for all user studies
- Apply iterative design process

## How to Run

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Mikuu177/qt-cw-vedio.git
cd qt-cw-vedio
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

From the project root directory:
```bash
python src/main.py
```

### Keyboard Shortcuts

- **Space**: Play/Pause
- **Left/Right Arrow**: Seek backward/forward 5 seconds
- **Up/Down Arrow**: Increase/decrease volume
- **Ctrl+O**: Open video file
- **Ctrl+Q**: Quit application

## Current Status

### Iteration 1 - Code Complete ✅ | Documentation In Progress 🔄

#### Completed Features ✅
- [x] OpenCV-based video playback (better codec support)
- [x] Play, pause, stop controls
- [x] Fast-forward (+10s) and rewind (-10s) buttons
- [x] Variable playback speed (0.25x - 2x)
- [x] Timeline scrubbing with time display (MM:SS format)
- [x] Volume control with mute button
- [x] Fullscreen mode (F key or button)
- [x] Comprehensive keyboard shortcuts
- [x] File menu (open video, quit)
- [x] Auto-load sample video
- [x] Status bar feedback

#### Completed Documentation ✅
- [x] User scenarios (3 detailed scenarios: Teacher, Student, Amateur)
- [x] Scoping analysis (MoSCoW prioritization, technical feasibility)
- [x] Project structure and README

#### In Progress 🔄
- [ ] UI/UX theory research document
- [ ] Ethics documentation templates
- [ ] Heuristic evaluation (recruiting participants)
- [ ] Iteration video 1 (45s-1m20s)

### Iteration 2 - Planned 📋
- Video editing features (trim, cut, multi-clip timeline)
- FFmpeg integration for video processing
- Marker system for navigation
- Enhanced accessibility (high contrast mode)
- Cognitive walkthrough evaluation
- Iteration video 2

### Iteration 3 - Planned 📋
- Internationalization (English/Chinese)
- Export functionality with quality options
- Undo/redo system (Command pattern)
- Performance optimization
- SUS questionnaire evaluation
- Iteration video 3 + Showcase video

## License
Academic project for University of Leeds - XJCO2811

## Acknowledgments
Based on the Tomeo application framework
