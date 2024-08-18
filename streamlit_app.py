import streamlit as st
import soundfile as sf
from pathlib import Path
import base64
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# Define the notes and their corresponding files
NOTE_FILES = {
    # Octave 4 (placeholders, uncomment and add files when ready)
    # 'C4': 'notes/c4.wav',
    # 'C#4': 'notes/c_sharp_4.wav',
    # 'D4': 'notes/d4.wav',
    # 'D#4': 'notes/d_sharp_4.wav',
    # 'E4': 'notes/e4.wav',
    # 'F4': 'notes/f4.wav',
    # 'F#4': 'notes/f_sharp_4.wav',
    # 'G4': 'notes/g4.wav',
    # 'G#4': 'notes/g_sharp_4.wav',
    # 'A4': 'notes/a4.wav',
    # 'A#4': 'notes/a_sharp_4.wav',
    # 'B4': 'notes/b4.wav',

    # Octave 5 (placeholders, uncomment and add files when ready)
    # 'C5': 'notes/c5.wav',
    # 'C#5': 'notes/c_sharp_5.wav',
    # 'D5': 'notes/d5.wav',
    # 'D#5': 'notes/d_sharp_5.wav',
    # 'E5': 'notes/e5.wav',
    # 'F5': 'notes/f5.wav',
    # 'F#5': 'notes/f_sharp_5.wav',
    # 'G5': 'notes/g5.wav',
    # 'G#5': 'notes/g_sharp_5.wav',
    # 'A5': 'notes/a5.wav',
    # 'A#5': 'notes/a_sharp_5.wav',
    # 'B5': 'notes/b5.wav',

    # Octave 6 (active keys with sound files)
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
        audio_file = open(file, 'rb')
        audio_bytes = audio_file.read()
        base64_audio = base64.b64encode(audio_bytes).decode()

        audio_html = f"""
        <audio id="audio" autoplay>
        <source src="data:audio/wav;base64,{base64_audio}" type="audio/wav">
        Your browser does not support the audio element.
        </audio>
        <script>
        document.getElementById('audio').play();
        </script>
        """
        components.html(audio_html, height=0, width=0)
    else:
        pass

# CSS for a more realistic piano look
piano_style = """
    <style>
    .white-key {
        background-color: white;
        border: 1px solid black;
        width: 60px;
        height: 200px;
        display: inline-block;
        margin: 0 -4px;
        position: relative;
        z-index: 1;
    }
    .black-key {
        background-color: black;
        border: 1px solid black;
        width: 40px;
        height: 120px;
        display: inline-block;
        margin: 0 -20px;
        position: relative;
        top: 0;
        z-index: 2;
    }
    .key-container {
        display: inline-block;
        position: relative;
        margin: 0;
    }
    </style>
    """

# Display styles
st.markdown(piano_style, unsafe_allow_html=True)

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

# Render the keys horizontally with proper overlap
st.title("Piano App")
st.markdown('<div style="display:flex; justify-content:center;">', unsafe_allow_html=True)
for i, (note, style, is_active) in enumerate(keys_layout):
    if is_active:
        if st.button("▶", key=note, help=f"Play {note}", use_container_width=True):
            play_note(note)
    else:
        st.button("▶", key=note, disabled=True, use_container_width=True)
    st.markdown(f'<div class="key-container"><div class="{style}"></div></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
