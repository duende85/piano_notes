import streamlit as st
import base64
import random
from pathlib import Path

st.set_page_config(layout="wide")

# Notes and their corresponding files
NOTE_FILES = {
    'C6': 'notes/c6.wav',
    'C#6': 'notes/c_sharp_6.wav',
    'D6': 'notes/d6.wav',
    'D#6': 'notes/d_sharp_6.wav',
    'E6': 'notes/e6.wav',
    'F6': 'notes/f6.wav',
    'G6': 'notes/g6.wav',
    'G#6': 'notes/g_sharp_6.wav',
    'A6': 'notes/a6.wav',
    'A#6': 'notes/a_sharp_6.wav',
    'B6': 'notes/b6.wav',
}

KEY_SCORES = {
    'C6': 'key_scores/c6.png',
    'C#6': 'key_scores/c_sharp_6.png',
    'D6': 'key_scores/d6.png',
    'D#6': 'key_scores/d_sharp_6.png',
    'E6': 'key_scores/e6.png',
    'F6': 'key_scores/f6.png',
    'G6': 'key_scores/g6.png',
    'G#6': 'key_scores/g_sharp_6.png',
    'A6': 'key_scores/a6.png',
    'A#6': 'key_scores/a_sharp_6.png',
    'B6': 'key_scores/b6.png',
}

# Initialize session state if not already set
if 'current_key' not in st.session_state:
    st.session_state.current_key = random.choice(list(KEY_SCORES.keys()))

if 'feedback_message' not in st.session_state:
    st.session_state.feedback_message = ""

if 'audio_data' not in st.session_state:
    st.session_state.audio_data = {}

# Function to play the note
def play_note_and_animate(note):
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
        <script>
        var keyElement = document.getElementById('{note}');
        keyElement.classList.add('pressed');
        setTimeout(function() {{
            keyElement.classList.remove('pressed');
        }}, 2000);
        </script>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
    else:
        st.warning(f"Note file for {note} not found.")

# Function to check if the pressed key matches the displayed key
def check_key_press(note):
    if note == st.session_state.current_key:
        st.session_state.feedback_message = "Correct!"
        st.session_state.feedback_color = "green"
    else:
        st.session_state.feedback_message = "Incorrect"
        st.session_state.feedback_color = "red"

# Styling for keys
white_key_style = """
    <style>
    .white-key {
        background-color: white;
        color: black;
        border: 1px solid black;
        width: 60px;
        height: 200px;
        display: inline-block;
        margin-right: -2px;
        z-index: 1;
        transition: transform 0.1s ease;
    }
    .white-key.pressed {
        background-color: lightgray;
        transform: translateY(5px);
    }
    .white-key .label {
        position: absolute;
        bottom: 5px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 14px;
    }
    </style>
    """

black_key_style = """
    <style>
    .black-key {
        background-color: black;
        color: white;
        border: 1px solid black;
        width: 40px;
        height: 120px;
        display: inline-block;
        position: absolute;
        margin-left: -20px;
        z-index: 3;
        top: 0;
        transition: transform 0.1s ease;
    }
    .black-key.pressed {
        background-color: darkgray;
        transform: translateY(5px);
    }
    </style>
    """

# Display styles
st.markdown(white_key_style, unsafe_allow_html=True)
st.markdown(black_key_style, unsafe_allow_html=True)

# Display the current key's image
st.title("Score Sync App / Igor Wilk / August 2024")
current_image_path = KEY_SCORES[st.session_state.current_key]

try:
    st.image(current_image_path, use_column_width=False)
except Exception as e:
    st.error(f"Error displaying image: {e}")
    st.write(f"Currently selected note: {st.session_state.current_key}")  # Fallback to text

# Display the piano keys
columns = st.columns(14)
keys = [
    ("C", "white"),
    ("C#", "black"),
    ("D", "white"),
    ("D#", "black"),
    ("E", "white"),
    ("F", "white"),
    ("F#", "black"),
    ("G", "white"),
    ("G#", "black"),
    ("A", "white"),
    ("A#", "black"),
    ("B", "white")
]

# Adjust the button layout for the piano keys
for i, (note, style) in enumerate(keys):
    with columns[i]:
        full_note = f"{note}6"  # Adjust octave as needed
        if st.button("▶", key=full_note):
            play_note_and_animate(full_note)
            check_key_press(full_note)
        key_html = f'<div id="{full_note}" class="{style}-key"></div>'
        st.markdown(key_html, unsafe_allow_html=True)

# Display feedback message
if st.session_state.feedback_message:
    st.markdown(f"<h3 style='color:{st.session_state.feedback_color};'>{st.session_state.feedback_message}</h3>", unsafe_allow_html=True)

# Manual refresh button for the note score
if st.button("Refresh Note Score"):
    st.session_state.current_key = random.choice(list(KEY_SCORES.keys()))
    st.session_state.feedback_message = ""

st.markdown("## Write anything you want below the piano here.")
st.write("This is where you can add any text, charts, or other content you want to display below the piano visualization.")
