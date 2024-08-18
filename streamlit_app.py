import streamlit as st
import base64
import random
from pathlib import Path

st.set_page_config(layout="wide")

# Custom CSS to reduce whitespace and ensure proper key alignment
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    .white-key {
        background-color: white;
        color: black;
        border: 1px solid black;
        width: 60px;
        height: 200px;
        display: inline-block;
        margin-right: -4px; /* Tighter spacing to reduce gaps */
        z-index: 1;
        position: relative;
        transition: transform 0.1s ease;
    }
    .black-key {
        background-color: black;
        color: white;
        border: 1px solid black;
        width: 40px;
        height: 120px;
        display: inline-block;
        position: absolute;
        margin-left: -20px;
        z-index: 2; /* Black keys are positioned above white keys */
        top: 0;
        transition: transform 0.1s ease;
    }
    .stButton button {
        font-size: 10px;
        padding: 3px 6px;
    }
    .piano-container {
        display: flex;
        flex-wrap: nowrap;
        justify-content: center;
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

# Function to generate keys layout
def generate_keys_layout(octave_range):
    keys_layout = []
    for octave in octave_range:
        for note in ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']:
            key_name = f'{note}{octave}'
            style = 'black-key' if '#' in note else 'white-key'
            label = 'C4' if key_name == 'C4' else ''
            keys_layout.append((key_name, style, label))
    return keys_layout

# Define the layout for the keys (Octave 4 only for simplicity)
keys_layout = generate_keys_layout(octave_range=[4])

# Render the keys horizontally in a piano container
st.title("Score Sync App / Igor Wilk / August 2024")
st.markdown("<div class='piano-container'>", unsafe_allow_html=True)
for note, style, label in keys_layout:
    if st.button("▶", key=note):
        play_note_if_correct(note)
    
    # Display the key with the note ID and add label if it's C4
    key_html = f'<div id="{note}" class="{style}">'
    if label:
        key_html += f'<div class="label">{label}</div>'
    key_html += '</div>'
    st.markdown(key_html, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Display feedback message
if st.session_state.feedback_message:
    st.markdown(f"<h3 style='color:{st.session_state.feedback_color};'>{st.session_state.feedback_message}</h3>", unsafe_allow_html=True)

# Manual refresh button for the note score
if st.button("Refresh Note Score"):
    # Resetting the entire app state
    st.session_state.current_key = random.choice(list(KEY_SCORES.keys()))
    st.session_state.feedback_message = ""
