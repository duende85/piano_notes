import streamlit as st
import base64
import random
from pathlib import Path

st.set_page_config(layout="wide")

# Custom CSS to reduce whitespace
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    </style>
    """, unsafe_allow_html=True)

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

if 'key_colors' not in st.session_state:
    st.session_state.key_colors = {key: "white" if '#' not in key else "black" for key in NOTE_FILES.keys()}

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
        """
        st.markdown(audio_html, unsafe_allow_html=True)
    else:
        st.warning(f"Note file for {note} not found.")

# Function to check if the pressed key matches the displayed key and set colors
def check_key_press(note):
    if note == st.session_state.current_key:
        st.session_state.key_colors[note] = "green"
    else:
        st.session_state.key_colors[note] = "red"
        st.session_state.key_colors[st.session_state.current_key] = "green"  # Mark correct key

# Styling for keys, updated dynamically based on key_colors
def get_key_style(note):
    background_color = st.session_state.key_colors[note]
    if '#' in note:
        return f"""
        <style>
        .black-key-{note} {{
            background-color: {background_color};
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
        }}
        .black-key-{note}.pressed {{
            background-color: darkgray;
            transform: translateY(5px);
        }}
        </style>
        """
    else:
        return f"""
        <style>
        .white-key-{note} {{
            background-color: {background_color};
            color: black;
            border: 1px solid black;
            width: 60px;
            height: 200px;
            display: inline-block;
            margin-right: -2px;
            z-index: 1;
            transition: transform 0.1s ease;
        }}
        .white-key-{note}.pressed {{
            background-color: lightgray;
            transform: translateY(5px);
        }}
        </style>
        """

# Render the keys horizontally
st.title("Score Sync App / Igor Wilk / August 2024")
current_image_path = KEY_SCORES[st.session_state.current_key]
st.image(current_image_path, use_column_width=False)

columns = st.columns(12)
notes = ['C6', 'C#6', 'D6', 'D#6', 'E6', 'F6', 'F#6', 'G6', 'G#6', 'A6', 'A#6', 'B6']

for i, note in enumerate(notes):
    with columns[i]:
        style = get_key_style(note)
        st.markdown(style, unsafe_allow_html=True)

        if st.button("▶", key=note):
            play_note_and_animate(note)
            check_key_press(note)
        
        key_class = f"black-key-{note}" if '#' in note else f"white-key-{note}"
        key_html = f'<div id="{note}" class="{key_class}"></div>'
        st.markdown(key_html, unsafe_allow_html=True)

# Manual refresh button for the note score
if st.button("Refresh Note Score"):
    st.session_state.current_key = random.choice(list(KEY_SCORES.keys()))
    st.session_state.feedback_message = ""
    # Reset key colors
    st.session_state.key_colors = {key: "white" if '#' not in key else "black" for key in NOTE_FILES.keys()}
