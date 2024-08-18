import streamlit as st
import soundfile as sf
from pathlib import Path
import base64
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# Define the notes and their corresponding files
NOTE_FILES = {
    # Octave 3
    # 'C3': 'notes/c3.wav',
    # 'C#3': 'notes/c_sharp_3.wav',
    # 'D3': 'notes/d3.wav',
    # 'D#3': 'notes/d_sharp_3.wav',
    # 'E3': 'notes/e3.wav',
    # 'F3': 'notes/f3.wav',
    # 'F#3': 'notes/f_sharp_3.wav',
    # 'G3': 'notes/g3.wav',
    # 'G#3': 'notes/g_sharp_3.wav',
    # 'A3': 'notes/a3.wav',
    # 'A#3': 'notes/a_sharp_3.wav',
    # 'B3': 'notes/b3.wav',

    # Octave 4
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

    # Octave 5
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

    # Octave 7 (future extension)
    # 'C7': 'notes/c7.wav',
    # 'C#7': 'notes/c_sharp_7.wav',
    # 'D7': 'notes/d7.wav',
    # 'D#7': 'notes/d_sharp_7.wav',
    # 'E7': 'notes/e7.wav',
    # 'F7': 'notes/f7.wav',
    # 'F#7': 'notes/f_sharp_7.wav',
    # 'G7': 'notes/g7.wav',
    # 'G#7': 'notes/g_sharp_7.wav',
    # 'A7': 'notes/a7.wav',
    # 'A#7': 'notes/a_sharp_7.wav',
    # 'B7': 'notes/b7.wav',
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

# Styling keys to resemble piano keys
white_key_style = """
    <style>
    .white-key {
        background-color: white;
        color: black;
        border: 1px solid black;
        width: 50px;
        height: 150px;
        display: inline-block;
        text-align: center;
        line-height: 150px;
        font-size: 20px;
        margin: 0 2px;
    }
    </style>
    """

black_key_style = """
    <style>
    .black-key {
        background-color: black;
        color: white;
        border: 1px solid black;
        width: 35px;
        height: 100px;
        display: inline-block;
        text-align: center;
        line-height: 100px;
        font-size: 16px;
        margin: 0 -17px;
        position: relative;
        z-index: 1;
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

# Render the keys
st.title("Piano App")
st.write("<div>", unsafe_allow_html=True)

for note, style in keys_layout:
    if st.button(note, key=note):
        play_note(note)
    st.markdown(f'<div class="{style}">{note}</div>', unsafe_allow_html=True)

st.write("</div>", unsafe_allow_html=True)
