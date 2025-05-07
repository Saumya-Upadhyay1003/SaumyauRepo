# SaumyauRepo
# 🎤 AI Interview Coach (Voice-Based)

An AI-powered mock interview tool built with Streamlit that allows users to:

✅ Generate personalized Product Manager interview questions from their resume  
🎙️ Record 2.5-minute voice answers  
🧠 Get AI-generated feedback — including a rating out of 10  
📈 See a waveform of their recorded answer  
⏳ Watch a live countdown while speaking

---

## 🚀 Features

- **Resume-based personalized questions** (GPT-generated)
- **Voice input** using microphone (2.5 minutes per answer)
- **Speech-to-text transcription** using OpenAI Whisper
- **AI feedback** with scoring out of 10 (GPT-3.5-turbo)
- **Countdown timer** during recording
- **Audio waveform visualization**

---

## 🛠 Tech Stack

- [Streamlit](https://streamlit.io) for UI
- [OpenAI GPT-3.5](https://platform.openai.com) for question generation & feedback
- [OpenAI Whisper](https://platform.openai.com/docs/guides/speech-to-text) for transcription
- [Sounddevice](https://python-sounddevice.readthedocs.io) for voice recording
- [Matplotlib](https://matplotlib.org/) for waveform visualization

---

## 🔐 API Key Setup

Store your OpenAI API key securely using Streamlit secrets:

```bash
OPENAI_API_KEY = sk-proj-xxxxxxxxxxxxxxxxxxxxxxxx
