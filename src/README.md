# Source Code

## Structure
- `main.py` - Application entry point
- `/ui` - User interface components
  - `main_window.py` - Main application window with video player
- `/video` - Video processing and playback logic (to be implemented in Iteration 2)
- `/utils` - Utility functions and helpers (to be added as needed)

## Development Guidelines
- Follow Qt coding conventions
- Comment complex logic with HCI principle rationale
- Keep UI and business logic separated
- Write modular, reusable code
- All UI code should reference relevant HCI principles (for report documentation)

## How to Run

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Install dependencies:
```bash
cd qt-cw-vedio
pip install -r requirements.txt
```

### Running the Application

From the project root directory:
```bash
python src/main.py
```

Or from the src directory:
```bash
cd src
python main.py
```

## Keyboard Shortcuts (Iteration 1)

- **Space**: Play/Pause
- **Left Arrow**: Seek backward 5 seconds
- **Right Arrow**: Seek forward 5 seconds
- **Up Arrow**: Increase volume
- **Down Arrow**: Decrease volume
- **F**: Toggle fullscreen
- **M**: Toggle mute
- **Escape**: Exit fullscreen (when in fullscreen mode)
- **Ctrl+O**: Open video file
- **Ctrl+Q**: Quit application

## Current Features (Iteration 1)

### Playback Controls
- Basic video playback (play, pause, stop)
- Fast-forward (+10s) and rewind (-10s) buttons
- Variable playback speed (0.25x, 0.5x, 0.75x, 1x, 1.25x, 1.5x, 2x)
- Timeline scrubbing with time display
- Volume control with mute button

### Display Features
- Fullscreen mode support
- Responsive video display
- Time display (current/total in MM:SS format)

### Accessibility
- Comprehensive keyboard shortcuts for all functions
- Clear visual feedback for all controls
- Tooltip hints on all buttons
- Auto-load sample video for testing

## Planned Features

### Iteration 2
- Video trimming/cutting
- Multi-clip timeline
- Marker system
- Basic filters
- High contrast mode
- Enhanced accessibility

### Iteration 3
- Internationalization (English/Chinese)
- Export functionality
- Undo/redo system
- Performance optimization
