import streamlit as st
import openai
import os
import uuid
import sounddevice as sd
from scipy.io.wavfile import write
import time
import matplotlib.pyplot as plt

# ✅ Secure API key from Streamlit Secrets
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize session state
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0
if 'interview_started' not in st.session_state:
    st.session_state.interview_started = False
if 'resume_summary' not in st.session_state:
    st.session_state.resume_summary = ""

st.title("🎤 AI Interview Coach (2.5-Min Answer + Feedback)")

# Step 1: Resume Summary Input
st.subheader("📄 Paste Your Resume Summary:")
resume_input = st.text_area("This will be used to generate personalized interview questions.", height=200)
start_button = st.button("🚀 Start Interview")

# Step 2: Generate Questions
if start_button:
    if not resume_input.strip():
        st.warning("Please paste a resume summary to start.")
    else:
        st.session_state.resume_summary = resume_input
        prompt = f"""
        You are a professional interview coach. Based on the following resume summary, generate 5 interrelated Product Manager interview questions.

        Resume Summary: {resume_input}

        Make the questions progressively deeper (e.g., roadmap → metrics → collaboration → failures → innovation). Return them as a numbered list.
        """
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        q_text = response.choices[0].message.content
        st.session_state.questions = [
            line[3:].strip()
            for line in q_text.split("\n")
            if line.strip() and (line.strip().startswith("1.") or line.strip()[0].isdigit())
        ]
        st.session_state.interview_started = True
        st.session_state.question_index = 0

# Step 3: Interview Loop
if st.session_state.interview_started and st.session_state.question_index < len(st.session_state.questions):
    current_q = st.session_state.questions[st.session_state.question_index]
    st.subheader(f"🧠 Question {st.session_state.question_index + 1}:")
    st.write(current_q)

    fs = 16000         # Sample rate (optimized for Whisper)
    duration = 150     # 2.5 minutes = 150 seconds

    st.markdown("🎙️ Click to record your answer (max 2.5 minutes).")

    if st.button("🎤 Start Recording"):
        try:
            st.info("Recording started. Speak clearly.")
            recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)

            # Countdown timer
            timer_placeholder = st.empty()
            for i in range(duration, 0, -1):
                timer_placeholder.markdown(f"⏳ Recording... **{i} seconds left**")
                time.sleep(1)

            sd.wait()
            temp_path = f"{str(uuid.uuid4())}.wav"
            write(temp_path, fs, recording)
            st.success("Recording complete.")

            # Display waveform
            fig, ax = plt.subplots()
            ax.plot(recording)
            ax.set_title("🎧 Your Recorded Audio Waveform")
            st.pyplot(fig)

            # Transcribe
            st.info("Transcribing your answer...")
            with open(temp_path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
                answer = transcript.text
            os.remove(temp_path)

            st.subheader("📝 Your Answer:")
            st.write(answer)

            # GPT Feedback with rating out of 10
            feedback_prompt = f"""
            Resume: {st.session_state.resume_summary}
            Question: {current_q}
            Answer: {answer}

            Please provide professional interview feedback including:
            1. Clarity and completeness
            2. Structure and logic (e.g., STAR)
            3. Product/domain insight
            4. Tone, confidence, ownership
            5. Suggestions to improve

            Conclude with an overall rating out of 10.
            """
            st.info("Analyzing your answer...")
            feedback_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": feedback_prompt}]
            )
            feedback = feedback_response.choices[0].message.content
            st.subheader("🔍 Interview Coach Feedback:")
            st.write(feedback)

            if st.button("➡️ Next Question"):
                st.session_state.question_index += 1

        except Exception as e:
            st.error(f"Something went wrong: {e}")

elif st.session_state.interview_started:
    st.success("✅ Interview complete! You’ve answered all questions.")

# End session
if st.session_state.interview_started and st.button("⛔ End Interview"):
    st.session_state.interview_started = False
    st.session_state.questions = []
    st.session_state.question_index = 0
    st.session_state.resume_summary = ""
    st.success("Interview session ended.")
