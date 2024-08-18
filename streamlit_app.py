import streamlit as st
import soundfile as sf
from pathlib import Path
import base64
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# Define the notes and their corresponding files
NOTE_FILES = {
    # Octave 6
    'C6': 'notes/c6.wav',
    'C#6': 'notes/c_sharp_6.wav',
    'D6': 'notes/d6.wav',
    'D#6': 'notes/d_sharp_6.wav',
    'E6': 'notes/e6.wav',
    'F6': 'notes/f6.wav',
    'F#6': 'notes/f_sharp_6.wav',
    'G6': 'notes/g6.wav',
    'G#6': 'notes/g_sharp_6.wav',
    'A6': 'notes/a6.wav',
    'A#6': 'notes/a_sharp_6.wav',
    'B6': 'notes/b6.wav',
}

def play_note(note):
    file = NOTE_FILES.get(note)
    if file and Path(file).exists():
        st.audio(file, format='audio/wav')

# Styling keys to resemble piano keys
white_key_style = """
    <style>
    .white-key {
        background-color: white;
        color: black;
        border: 1px solid black;
        width: 60px;
        height: 200px;
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 2px;
        cursor: pointer;
    }
    .white-key:active {
        transform: translateY(5px);
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
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 -20px;
        z-index: 2;
        position: relative;
        cursor: pointer;
    }
    .black-key:active {
        transform: translateY(5px);
    }
    </style>
    """

# Display styles
st.markdown(white_key_style, unsafe_allow_html=True)
st.markdown(black_key_style, unsafe_allow_html=True)

# Define the layout for the keys
keys_layout = [
    ('C6', 'white-key'), ('C#6', 'black-key'), ('D6', 'white-key'), ('D#6', 'black-key'), 
    ('E6', 'white-key'), ('F6', 'white-key'), ('F#6', 'black-key'), ('G6', 'white-key'), 
    ('G#6', 'black-key'), ('A6', 'white-key'), ('A#6', 'black-key'), ('B6', 'white-key')
]

# Render the keys horizontally
st.title("Piano App")
columns = st.columns(len(keys_layout))

for i, (note, style) in enumerate(keys_layout):
    with columns[i]:
        if st.button(note, key=note, help=f"Play {note}"):
            play_note(note)
        st.markdown(f'<div class="{style}"></div>', unsafe_allow_html=True)
