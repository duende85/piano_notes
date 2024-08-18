import streamlit as st
import soundfile as sf
from pathlib import Path
import base64
import streamlit.components.v1 as components
import time

st.set_page_config(layout="wide")

# Define the notes and their corresponding files
NOTE_FILES = {
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

# Function to play the note and temporarily change the key's appearance
def play_note_and_animate(note):
    file = NOTE_FILES.get(note)
    if file and Path(file).exists():
        audio_file = open(file, 'rb')
        audio_bytes = audio_file.read()
        base64_audio = base64.b64encode(audio_bytes).decode()

        audio_html = f"""
        <audio id="audio" autoplay>
        <source src="data:audio/wav;base64,{base64_audio}" type="audio/wav">
        Your browser does not support the audio element.
        </audio>
        <script>
        document.getElementById('{note}').classList.add('pressed');
        setTimeout(function() {{
            document.getElementById('{note}').classList.remove('pressed');
        }}, 2000);
        </script>
        """
        components.html(audio_html, height=0, width=0)
    else:
        pass

# Styling keys to resemble piano keys
white_key_style = """
    <style>
    .white-key {
        background-color: white;
        color: black;
        border: 1px solid black;
        width: 60px;
        height: 200px;
        display: inline-block;
        position: relative;
        margin-right: -2px;
        z-index: 1;
    }
    .white-key.pressed {
        background-color: lightgray;
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
        display: inline-block;
        position: absolute;
        margin-left: -20px;
        z-index: 2;
        top: 0;
    }
    .black-key.pressed {
        background-color: darkgray;
        transform: translateY(5px);
    }
    </style>
    """

# Adjust the button size and remove space between columns
button_style = """
    <style>
    .stButton button {
        font-size: 10px;
        padding: 3px 6px;
    }
    .stColumn > div {
        padding: 0px;
    }
    </style>
    """

# Display styles
st.markdown(white_key_style, unsafe_allow_html=True)
st.markdown(black_key_style, unsafe_allow_html=True)
st.markdown(button_style, unsafe_allow_html=True)

# Function to generate keys layout
def generate_keys_layout(octave_range, active_octave=None):
    keys_layout = []
    for octave in octave_range:
        for note in ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']:
            key_name = f'{note}{octave}'
            style = 'black-key' if '#' in note else 'white-key'
            is_active = octave == active_octave and key_name in NOTE_FILES
            keys_layout.append((key_name, style, is_active))
    return keys_layout

# Define the layout for the keys (Octaves 4, 5, 6)
keys_layout = generate_keys_layout(octave_range=range(4, 7), active_octave=6)

# Render the keys horizontally
st.title("Piano App")
columns = st.columns(len(keys_layout))

for i, (note, style, is_active) in enumerate(keys_layout):
    with columns[i]:
        if is_active:
            if st.button("▶", key=note, help=f"Play {note}"):
                play_note_and_animate(note)
        else:
            st.button("▶", key=note, disabled=True)
        
        # Display the key with the note ID
        st.markdown(f'<div id="{note}" class="{style}"></div>', unsafe_allow_html=True)
