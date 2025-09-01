# 情绪调节实验 | Emotion Regulation Experiment

A complete jsPsych 8-based emotion regulation experiment with cognitive reappraisal paradigm.

## 🚀 Quick Start

1. **Start a local server:**
   ```bash
   # Python
   python -m http.server 8080
   
   # OR Node.js
   npx http-server -p 8080
   ```

2. **Open in browser:**
   ```
   http://localhost:8080/experiment.html
   ```

## 📁 Simple Structure

```
eye-tracking-emotion-experiment/
├── experiment.html         # The complete experiment (single file)
├── assets/
│   └── images/            # Your stimulus images
│       ├── H(1-3).jpg     # Practice high arousal
│       ├── L(1-3).jpg     # Practice low arousal
│       └── (1-28).jpg     # Formal experiment images
└── README.md              # This file
```

## 🎯 Experiment Design

### Participant Information
The experiment begins with a participant information form collecting:
- Participant ID
- Age
- Gender
- Notes (optional)

### Trial Structure (6 steps per block)
1. **Fixation** (+) - 2 seconds
2. **Strategy Instruction** - User-controlled (认知重评 or 自然观看)
3. **Preparation** - 2 seconds
4. **Image Presentation** - 8 seconds
5. **Rating Scale** - User-controlled (1-7 scale)
6. **Blank Screen** - 2 seconds

### Phases
- **Practice**: 6 blocks for familiarization
- **Formal**: 28 blocks with balanced conditions
- **Rest Break**: 2-minute break at midpoint (spacebar to skip)

## 📊 Data Output

Automatically saves CSV file named: `emotion_regulation_[ParticipantID]_[timestamp].csv`

Contains:
- Participant demographic information
- Rating responses (1-7)
- Reaction times
- Strategy type per trial
- Image names
- Block numbers
- Experiment timestamp

## ⚙️ Configuration

Edit these values in `experiment.html`:

```javascript
const CONFIG = {
    ASSET_PATH: './assets/images/',
    EXPERIMENT_NAME: 'emotion_regulation',
    REST_DURATION: 120000, // 2 minutes
    ALLOW_REST_SKIP: true
};
```

## 📋 Requirements

- Modern browser (Chrome/Edge/Firefox)
- Local web server (for security)
- Stimulus images in `assets/images/`

## 🔧 Troubleshooting

### Images not loading?
- Check browser console (F12)
- Verify images exist in `assets/images/`
- Ensure correct file extensions (.jpg/.JPG)

### Data not saving?
- Enable browser pop-ups
- Check downloads folder

## 📈 Features

✅ Interactive rating scales  
✅ User-controlled progression  
✅ Progress bar  
✅ Automatic data export  
✅ Summary statistics  
✅ Fullscreen mode  
✅ Rest break with timer  

## 📝 Citation

```
Emotion Regulation Experiment
jsPsych 8.0.2 Implementation
```