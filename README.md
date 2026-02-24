<div align="center">

# 🧠 Maitri AI

### *Multimodal Emotion-Aware Conversational Assistant*

[![Python](https://img.shields.io/badge/Python-3.13%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![TensorFlow](https://img.shields.io/badge/TensorFlow_Lite-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://tensorflow.org/lite)
[![Groq](https://img.shields.io/badge/Groq_LLM-Llama_3.3_70B-F55036?style=for-the-badge)](https://groq.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)

**Maitri AI** is a real-time emotionally intelligent assistant that fuses **facial emotion recognition**, **speech sentiment analysis**, and **LLM-based reasoning** to deliver empathetic, context-aware responses — understanding not just *what* you say, but *how* you feel when you say it.

</div>



## 🌟 What Makes Maitri Different

Most AI assistants process only text. Maitri AI perceives you across **three simultaneous channels**:

| Channel | What It Captures | How |
|---------|-----------------|-----|
| 👁️ **Face** | Real-time emotional state | TFLite model via webcam |
| 🎙️ **Voice** | Sentiment & intensity from speech | Google SR + VADER |
| 💬 **Text** | Semantic meaning of your message | Groq Llama 3.3 70B |

These signals are fused into a unified emotional context that shapes every AI response — making Maitri empathetic by design, not by chance.

---

## ✨ Features

### 🎭 Face Emotion Recognition
- Live webcam capture with OpenCV face detection
- TensorFlow Lite model classifies 7 emotions: `anger`, `disgust`, `fear`, `happy`, `neutral`, `sad`, `surprise`
- Returns emotion label + confidence score per frame
- Logs results to `face_emotion_log.csv` for trend tracking

### 🎙️ Speech-to-Text + Sentiment
- Google Speech Recognition converts audio to text
- VADER sentiment engine scores polarity and emotional intensity
- Outputs: `positive / neutral / negative` + intensity level

### 💬 Emotion-Aware AI Chatbot
- Groq API (Llama 3.3 70B) receives a fused prompt containing:
  - Detected facial emotion + confidence
  - Voice sentiment + intensity
  - User's raw text input
- Responds with tone calibrated to the user's current emotional state

### 📊 Logging & Monitoring
- CSV logging of facial emotion history
- Text-based emotion event logs
- Automatic alert generation on sustained negative states
- Queryable via `/logs` and `/alerts` endpoints

---

## 🎬 Demo

> <img width="1916" height="864" alt="image" src="https://github.com/user-attachments/assets/56cb32ad-5274-4d0c-8f4f-ad60332b25a6" />

```
[webcam feed]          [chat interface]
    |                       |
  sad (0.87)     +   "I don't know what to do"
    |                       |
    └──────── Maitri AI ────┘
              ↓
  "It sounds like you're going through a tough time.
   Let's take this one step at a time together..."
```


##  Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Maitri AI System                     │
│                                                             │
│  ┌──────────┐    ┌──────────────────┐     ┌───────────────┐ │
│  │  Webcam  │───▶│  OpenCV + TFLite │───▶│ Emotion Label │ │
│  └──────────┘    │  Face Detection  │     │ + Confidence  │ │
│                  └──────────────────┘     └──────┬────────┘ │
│                                                  │          │
│  ┌──────────┐    ┌──────────────────┐     ┌──────▼────────┐ │
│  │   Mic    │───▶│  Google SR +     │───▶│   Sentiment   │ │
│  └──────────┘    │  VADER Analysis  │     │   + Intensity │ │
│                  └──────────────────┘     └──────┬────────┘ │
│                                                  │          │
│  ┌──────────┐                                    │          │
│  │  Text    │─────────────────────────────────▶  │          │
│  │  Input   │                             ┌──────▼────────┐ │
│  └──────────┘                             │  Fusion Layer │ │
│                                           └──────┬────────┘ │
│                                                 │           │
│                                           ┌──────▼────────┐ │
│                                           │  Groq LLM     │ │
│                                           │  Llama 3.3 70B│ │
│                                           └──────┬────────┘ │
│                                                 │           │
│                               ┌──────────────────▼────────┐ │
│                               │   Empathetic AI Response  │ │
│                               └───────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

##  Project Structure

```
version_6/
│
├── app.py                  # Flask app — routes, fusion logic, LLM calls
├── sentiment.py            # VADER sentiment analysis module
├── logger.py               # General emotion event logger
├── alert.py                # Alert generation for negative states
├── multimodal_logger.py    # Cross-modal logging coordinator
│
├── emotion_model.tflite    # Pretrained face emotion classification model
│
├── templates/
│   └── index.html          # Frontend — webcam + chat UI
│
├── face_emotion_log.csv    # Historical face emotion data
├── emotion_logs.txt        # Event-level emotion log
├── alerts.txt              # Generated alerts log

```



##  Setup

### Prerequisites
- Python 3.8+
- A webcam (for face emotion features)
- A [Groq API key](https://console.groq.com) (free tier available)

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/maitri-ai.git
cd maitri-ai
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install flask opencv-python tensorflow numpy speechrecognition vaderSentiment groq
```

### 4. Configure your API key

Open `app.py` and replace the placeholder:

```python
client = Groq(api_key="YOUR_GROQ_API_KEY_HERE")
```

>  For production use, store your key in a `.env` file and load it with `python-dotenv`.

### 5. Run the application

```bash
python app.py
```

Open your browser and navigate to: **http://127.0.0.1:5000**



##  API Reference

| Endpoint  | Method | Description                              |
|-----------|--------|------------------------------------------|
| `/`       | GET    | Main chat UI                             |
| `/chat`   | POST   | Send text; receives emotion-fused reply  |
| `/speech` | POST   | Submit audio; returns transcription + sentiment |
| `/predict`| POST   | Submit webcam frame; returns emotion label |
| `/logs`   | GET    | View full emotion event log              |
| `/alerts` | GET    | View generated alert history             |

### Example — `/chat` request

```json
POST /chat
{
  "message": "I feel completely overwhelmed today",
  "face_emotion": "sad",
  "face_confidence": 0.87,
  "speech_sentiment": "negative",
  "intensity": "high"
}
```

### Example — `/chat` response

```json
{
  "reply": "It sounds like today has been really heavy. That feeling of being overwhelmed is valid, and you don't have to navigate it alone. Would it help to talk through what's on your plate?",
  "detected_emotion": "sad",
  "sentiment": "negative"
}
```

---

##  Alert Logic

Alerts are automatically triggered when negative emotional states persist across multiple modalities:

```
Face: sad (confidence > 0.75)
 +
Speech: negative sentiment + high intensity
 ↓
→ Alert logged to alerts.txt
→ Viewable at /alerts
→ AI response switches to supportive mode
```

---

##  Emotion Fusion Example

```
Input signals:
  Facial emotion  →  sad       (confidence: 0.87)
  Speech sentiment →  negative  (intensity: high)
  User text       →  "I don't know what to do anymore"

Fused LLM prompt:
  "The user appears visually sad with high confidence.
   Their voice conveys negative sentiment at high intensity.
   Their message reads: 'I don't know what to do anymore.'
   Respond with empathy and gentle, supportive guidance."

AI Output:
  "That sounds incredibly hard. When everything feels uncertain,
   it can help to focus on just the next small step..."
```

---

##  Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend Framework | Flask |
| Face Detection | OpenCV |
| Emotion Classification | TensorFlow Lite |
| Speech Recognition | Google Speech Recognition |
| Sentiment Analysis | VADER (vaderSentiment) |
| LLM | Groq — Llama 3.3 70B |
| Logging | CSV + plaintext logs |
| Frontend | HTML / CSS / JavaScript |


##  Use Cases

- **Mental health support** — Gentle AI companionship calibrated to emotional state
- **Astronaut / isolated environment monitoring** — Emotional wellness checks
- **Therapy assistant tools** — Context-aware session support
- **Human-AI interaction research** — Multimodal emotion data collection
- **Smart companion applications** — Beyond keyword-matching, truly responsive AI

---

##  Contributing

Contributions are welcome! To get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

Please open an issue first for significant changes so we can discuss the approach.


##  Author

**Neithal Pillai**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/neithal-pillai-453a772b9/))


##  Team

Maitri AI was built by a team of 6 as a submission for **Makeathon** — a competitive hackathon focused on impactful innovation.

| Name 
|------
| **Neithal Pillai**  
| **Bhavyaa V**
| **Pranav K**
| **Dashetha N**
| **Dhavasi M**

>  *Built under hackathon conditions at **Makeathon** — from idea to working prototype as a team.*

---

##  License

This project is licensed under the **MIT License** — free to use, modify, and distribute.

See [LICENSE](LICENSE) for details.

---

<div align="center">

*Built with empathy, powered by multimodal AI.*
*A Makeathon hackathon project — crafted by a team of six.*

 If Maitri AI resonates with you, give it a star — it helps others find the project.

</div>
