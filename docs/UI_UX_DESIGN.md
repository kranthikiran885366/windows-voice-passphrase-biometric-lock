# User Interface & Experience Design

## Design Philosophy

**Cinematic. Authoritative. Secure.**

Inspired by Sivaji movie's computer security interface - dark, professional, with neon accents that convey advanced technology and trustworthiness.

## Color Palette

```
Primary Background:  #0a0e27  (Dark navy)
Primary Accent:      #00d9ff  (Cyan - "scanning" theme)
Secondary Accent:    #7c3aed  (Violet - "processing" theme)
Success:             #00ff66  (Green - "authorized")
Error:               #ff3333  (Red - "denied")

Text Primary:        #e0e0e0  (Light gray)
Text Secondary:      #b0b0b0  (Medium gray)
Border Glow:         #00d9ff  (Cyan)
```

## Typography

**Headings:**
- Font: Arial, sans-serif
- Size: 48px
- Weight: Bold
- Letter-spacing: 3px
- Transform: UPPERCASE
- Color: Cyan (#00d9ff)

**Body Text:**
- Font: Arial, sans-serif
- Size: 14-18px
- Weight: Regular
- Line-height: 1.6
- Color: Light gray (#e0e0e0)

**Monospace (Code/Values):**
- Font: Courier New
- Size: 12px
- Color: Cyan (#00d9ff)

## Layout

### Full-Screen Lockscreen

```
┌─────────────────────────────────────────────┐
│                                             │
│         SIVAJI                              │
│         VOICE BIOMETRIC AUTHENTICATION      │
│                                             │
├─────────────────────────────────────────────┤
│                                             │
│         VOICE AUTHENTICATION REQUIRED       │
│                                             │
│    ┌───────────────────────────────────┐   │
│    │ Speak: "The quick brown fox..."   │   │
│    │                                   │   │
│    │ [Animated Waveform]               │   │
│    │ ▁ ▂ ▃ ▄ ▅ ▆ █ ▆ ▅ ▄ ▃ ▂ ▁        │   │
│    │                                   │   │
│    │ Status: LISTENING...              │   │
│    │ Confidence: --                    │   │
│    │                                   │   │
│    │   [START AUTHENTICATION]          │   │
│    │                                   │   │
│    └───────────────────────────────────┘   │
│                                             │
│   Click START AUTHENTICATION and speak      │
│                                             │
└─────────────────────────────────────────────┘
```

### State Transitions

#### State 1: Idle (Ready)
```
Status: VOICE AUTHENTICATION REQUIRED
Button: [START AUTHENTICATION] (enabled)
Waveform: Static
Message: "Click START AUTHENTICATION and speak..."
```

#### State 2: Recording
```
Status: LISTENING...
Button: (disabled)
Waveform: Animated (color: cyan → violet)
Message: "Speak now. Recording..."
```

#### State 3: Processing
```
Status: ANALYZING VOICE...
Button: (disabled)
Waveform: Animated (fading out)
Message: "Processing biometric data..."
```

#### State 4A: Success
```
Status: ACCESS GRANTED (green, large)
Button: Hidden
Waveform: Visible with green glow
Message: "Authentication successful. [Green checkmark]"
[Auto-close after 2 seconds]
```

#### State 4B: Failure
```
Status: ACCESS DENIED (red, large)
Button: [START AUTHENTICATION] (enabled after 2s)
Waveform: Shows failure pattern (red)
Message: "Attempt 2/3 failed. Try again."
```

## Interactive Elements

### Button: START AUTHENTICATION

**Appearance:**
```
┌──────────────────────────┐
│ START AUTHENTICATION     │
└──────────────────────────┘

Background: #7c3aed (violet)
Text: White, bold, 12px
Border: 2px solid #00d9ff (cyan)
Padding: 12px 30px
Border-radius: 5px
```

**States:**
- **Default**: Violet bg, cyan border
- **Hover**: Darker violet, bright cyan border
- **Pressed**: Even darker violet
- **Disabled**: Grayed out (30% opacity)

**Interaction:**
```
Click → State transition to "Recording"
        Audio recording starts (3 seconds)
        Waveform animates
        Button disabled
```

### Waveform Visualization

**Purpose**: Real-time audio feedback during recording

**Visual:**
```
40 vertical bars (frequency bands)
Each bar height = audio intensity (0-100%)
Color gradient:
  - Cyan (#00d9ff): Quiet (< 30%)
  - Violet (#7c3aed): Medium (30-70%)
  - Red (#ff3333): Loud (> 70%)

Update rate: 50ms (20 FPS)
Animation: Smooth decay + sine wave modulation
```

**Example:**

```
Quiet period:         Medium level:         Loud period:
▂ ▂ ▂ ▂ ▂             ▃ ▅ ▇ █ ▇ ▅ ▃         ▄ ▆ █ █ ▆ ▄
```

### Status Indicators

**Text Labels:**
```
Status: "LISTENING..." (cyan, animated with dots)
        "ANALYZING VOICE..." (cyan → violet transition)
        "ACCESS GRANTED" (green, pulsing)
        "ACCESS DENIED" (red, shaking)

Confidence: "Confidence: 95.2% | Liveness: 87.5%"
            (Size, gray - updates during analysis)

Message: "Speak clearly and naturally"
         "Attempt 2/3 failed. Try again."
         (Below waveform, light gray)
```

## Microphone Indicator

**Visual**: 🎤 emoji (64px)

**Animation:**
- **Idle**: Static cyan
- **Recording**: Pulsing (scale 1.0 → 1.2)
- **Processing**: Rotating/spinning cyan
- **Success**: Static green with glow
- **Failure**: Static red with glow

## Dark Theme Implementation

### Background
```css
QMainWindow {
    background-color: #0a0e27;  /* Dark navy */
    color: #e0e0e0;             /* Light gray text */
}
```

### Benefits
- Reduces eye strain (especially late night)
- Conveys security/premium feel
- Better for neon accent colors
- Matches Sivaji cinema aesthetic

### Contrast Ratios
- Title (cyan on dark): 8.5:1 ✅ WCAG AAA
- Text (gray on dark): 4.5:1 ✅ WCAG AA
- Buttons (violet + cyan): 4.8:1 ✅ WCAG AA

## Animation Details

### Title Entrance
```
Duration: 800ms
Type: Fade-in + slide down
Timing: Ease-out cubic
```

### Button Hover
```
Duration: 200ms
Type: Background color + border color transition
Timing: Linear
```

### Waveform Update
```
Duration: Continuous
Type: Bar height animation + color transition
Frequency: 50ms per frame (20 FPS)
Easing: Linear (real-time audio)
```

### Success State
```
Duration: Pulsing (2s cycle)
Type: Green glow opacity change
Alpha: 0.5 → 1.0 → 0.5
Auto-close after: 2 seconds
```

### Failure State
```
Duration: 500ms
Type: Red background flash + shake
Intensity: Medium (±3px horizontal)
Repeat: 2 times
```

## Accessibility Features

### Keyboard Navigation
- ✅ All buttons keyboard accessible
- ✅ Tab order logical
- ✅ Enter/Space activate buttons
- ❌ System keys blocked for security

### Screen Reader Support
- ✅ ARIA labels on buttons
- ✅ Status updates announced
- ✅ Instruction text clear
- ⚠️ Animated waveform not described (decorative)

### Color Contrast
- ✅ All text meets WCAG AA (4.5:1)
- ✅ Title meets WCAG AAA (8.5:1)
- ✅ No color-only information

### Text Sizing
- ✅ Responsive to system text size setting
- ✅ No fixed px units (use relative)
- ✅ Readable at 150% zoom

## Responsive Design

### Desktop (1920x1080+)
```
Full-screen layout, centered
Max width: 800px dialog
Padding: 50px (comfortable)
```

### Laptop (1366x768)
```
Full-screen, slightly compressed
Max width: 600px
Padding: 30px
Font size: Reduced 10%
```

### Tablet (iPad-like)
```
Full-screen, portrait
Max width: 90% of screen
Font size: Adjusted for touch
Button size: 48px minimum (touch-friendly)
```

## Voice Bot Integration

### Success Voice Response
```
Text: "Authentication successful. Welcome. System access granted."
Timing: Plays immediately on auth success
Duration: ~3 seconds
Volume: 90% (professional, not annoying)
```

### Failure Voice Response
```
Text: "Unauthorized access detected. You are not permitted to use this system."
Timing: Plays immediately on auth failure
Duration: ~2.5 seconds
Volume: 90%
```

### Lockout Voice Response
```
Text: "Security violation confirmed. System locked."
Timing: Plays after 3rd failed attempt
Duration: ~1.5 seconds
Volume: 90%
```

## Future Design Enhancements

1. **3D Holographic-style Waveform**
   - WebGL/Three.js 3D visualization
   - Rotating spectrogram cube
   - More cinematic feel

2. **Gesture Recognition**
   - Swipe gestures on touch screens
   - Face detection animation

3. **Multi-language Support**
   - Auto-detect system language
   - Voice bot speaks in user's language
   - UI translatable

4. **Biometric Icon Animation**
   - Fingerprint-style radial animation
   - Flowing particles effect
   - More organic feel

5. **Accessibility Themes**
   - High contrast mode
   - Dyslexic-friendly fonts
   - Simplified UI option
