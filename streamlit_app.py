import streamlit as st
import base64
import random
from pathlib import Path

st.set_page_config(layout="wide")

# Custom CSS for piano layout
st.markdown("""
    <style>
    .piano-container {
        display: flex;
        justify-content: center;
        align-items: flex-start;
        width: 100%;
        position: relative;
        margin-top: 20px;
    }
    .white-key {
        width: 60px;
        height: 200px;
        background-color: white;
        border: 1px solid black;
        position: relative;
        z-index: 1;
        margin-right: -1px; /* Adjust to reduce gaps */
    }
    .black-key {
        width: 40px;
        height: 120px;
        background-color: black;
        border: 1px solid black;
        position: absolute;
        z-index: 2;
        margin-left: -20px; /* Adjust to position over white key */
        margin-top: 0px;
    }
    .black-key.C#4 { margin-left: 40px; }
    .black-key.D#4 { margin-left: 120px; }
    .black-key.F#4 { margin-left: 280px; }
    .black-key.G#4 { margin-left: 360px; }
    .black-key.A#4 { margin-left: 440px; }
    </style>
    """, unsafe_allow_html=True)

# Notes and their corresponding files
NOTE_FILES = {
    'C4': 'notes/c4.wav',
    'C#4': 'notes/c_sharp_4.wav',
    'D4': 'notes/d4.wav',
    'D#4': 'notes/d_sharp_4.wav',
    'E4': 'notes/e4.wav',
    'F4': 'notes/f4.wav',
    'F#4': 'notes/f_sharp_4.wav',
    'G4': 'notes/g4.wav',
    'G#4': 'notes/g_sharp_4.wav',
    'A4': 'notes/a4.wav',
    'A#4': 'notes/a_sharp_4.wav',
    'B4': 'notes/b4.wav',
}

KEY_SCORES = {
    'C4': 'key_scores/c4.png',
    'C#4': 'key_scores/c_sharp_4.png',
    'D4': 'key_scores/d4.png',
    'D#4': 'key_scores/d_sharp_4.png',
    'E4': 'key_scores/e4.png',
    'F4': 'key_scores/f4.png',
    'F#4': 'key_scores/f_sharp_4.png',
    'G4': 'key_scores/g4.png',
    'G#4': 'key_scores/g_sharp_4.png',
    'A4': 'key_scores/a4.png',
    'A#4': 'key_scores/a_sharp_4.png',
    'B4': 'key_scores/b4.png',
}

# Initialize session state if not already set
if 'current_key' not in st.session_state:
    st.session_state.current_key = random.choice(list(KEY_SCORES.keys()))

if 'feedback_message' not in st.session_state:
    st.session_state.feedback_message = ""

if 'audio_data' not in st.session_state:
    st.session_state.audio_data = {}

# Function to play the note (only when pressed correctly)
def play_note_if_correct(note):
    if note == st.session_state.current_key:
        file = NOTE_FILES.get(note)
        if file and Path(file).exists():
            if note not in st.session_state.audio_data:
                with open(file, 'rb') as audio_file:
                    audio_bytes = audio_file.read()
                    st.session_state.audio_data[note] = base64.b64encode(audio_bytes).decode()

            audio_html = f"""
            <audio autoplay>
            <source src="data:audio/wav;base64,{st.session_state.audio_data[note]}" type="audio/wav">
            Your browser does not support the audio element.
            </audio>
            """
            st.markdown(audio_html, unsafe_allow_html=True)

# Function to display the random image
def display_random_image():
    st.session_state.current_image = KEY_SCORES.get(st.session_state.current_key)
    st.image(st.session_state.current_image, use_column_width=False)

# Piano layout
st.title("Score Sync App / Igor Wilk / August 2024")
display_random_image()

st.markdown("<div class='piano-container'>", unsafe_allow_html=True)
white_notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4']
black_notes = ['C#4', 'D#4', 'F#4', 'G#4', 'A#4']

# Render white keys
for note in white_notes:
    st.markdown(f"<div class='white-key' onclick='playNote(\"{note}\")'></div>", unsafe_allow_html=True)
# Render black keys
for note in black_notes:
    st.markdown(f"<div class='black-key {note}' onclick='playNote(\"{note}\")'></div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# JavaScript for handling clicks
st.markdown("""
<script>
function playNote(note) {
    const streamlitEvent = new CustomEvent("streamlit-event", {
        detail: {note: note},
        bubbles: true,
        cancelable: true
    });
    window.dispatchEvent(streamlitEvent);
}
</script>
""", unsafe_allow_html=True)

# Check the pressed key and play the note if correct
if st.session_state.current_key:
    play_note_if_correct(st.session_state.current_key)

# Manual refresh button for the note score
if st.button("Refresh Note Score"):
    st.session_state.current_key = random.choice(list(KEY_SCORES.keys()))
    st.session_state.feedback_message = ""
