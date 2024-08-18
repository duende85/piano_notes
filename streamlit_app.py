import streamlit as st
import base64
import random
from pathlib import Path

st.set_page_config(layout="wide")

# Custom CSS for piano layout
st.markdown("""
    <style>
    .piano {
        display: flex;
        justify-content: center;
        position: relative;
        width: 800px; /* Adjust width as needed */
        margin: 0 auto;
    }
    .white-key, .black-key {
        position: relative;
        border: 1px solid black;
    }
    .white-key {
        width: 60px;
        height: 200px;
        background-color: white;
        z-index: 1;
    }
    .black-key {
        width: 40px;
        height: 120px;
        background-color: black;
        position: absolute;
        z-index: 2;
        top: 0;
        margin-left: -20px;
    }
    .white-key + .black-key { /* D#4 key placement */
        margin-left: 40px;
    }
    .white-key + .white-key {
        margin-left: -20px; /* Position white keys close together */
    }
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

# Function to play the note (only when pressed correctly)
def play_note_if_correct(note):
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

# Piano HTML layout
st.markdown("<div class='piano'>", unsafe_allow_html=True)

# Render white and black keys in HTML
for note in ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4']:
    st.markdown(f"<div class='white-key' onclick='playNote(\"{note}\")'></div>", unsafe_allow_html=True)
    if note in ['C4', 'D4', 'F4', 'G4', 'A4']:  # Add corresponding black keys
        black_note = f"{note[0]}#{note[1]}"
        st.markdown(f"<div class='black-key' onclick='playNote(\"{black_note}\")'></div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# JavaScript for playing notes
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

# Handle custom event
if 'current_key' not in st.session_state:
    st.session_state.current_key = random.choice(list(NOTE_FILES.keys()))

if 'feedback_message' not in st.session_state:
    st.session_state.feedback_message = ""

if 'audio_data' not in st.session_state:
    st.session_state.audio_data = {}

# Receive the note from the JavaScript event
if st.session_state.current_key:
    play_note_if_correct(st.session_state.current_key)

# Manual refresh button for the note score
if st.button("Refresh Note Score"):
    st.session_state.current_key = random.choice(list(NOTE_FILES.keys()))
    st.session_state.feedback_message = ""
