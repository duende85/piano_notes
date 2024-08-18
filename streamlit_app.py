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
    'F#6': 'notes/f_sharp_6.wav',
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
    'F#6': 'key_scores/f_sharp_6.png',
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
def generate_keys_layout(octave_range):
    keys_layout = []
    for octave in octave_range:
        for note in ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']:
            key_name = f'{note}{octave}'
            style = 'black-key' if '#' in note else 'white-key'
            label = 'C4' if key_name == 'C4' else ''
            keys_layout.append((key_name, style, label))
    return keys_layout

# Define the layout for the keys (Octaves 4, 5, 6)
keys_layout = generate_keys_layout(octave_range=range(4, 7))

# Current key being displayed
current_key = st.session_state.current_key
current_image_path = KEY_SCORES[current_key]

# Function to check if the pressed key matches the displayed key
def check_key_press(note):
    if note == current_key:
        st.session_state.feedback_message = "Correct!"
        st.session_state.feedback_color = "green"
    else:
        st.session_state.feedback_message = "Incorrect"
        st.session_state.feedback_color = "red"

# Render the keys horizontally
st.title("Score Sync App / Igor Wilk / August 2024")
st.image(current_image_path, use_column_width=False)
columns = st.columns(len(keys_layout))

for i, (note, style, label) in enumerate(keys_layout):
    with columns[i]:
        if st.button("▶", key=note):
            play_note_and_animate(note)
            check_key_press(note)
        
        # Display the key with the note ID and add label if it's C4
        key_html = f'<div id="{note}" class="{style}">'
        if label:
            key_html += f'<div class="label">{label}</div>'
        key_html += '</div>'
        st.markdown(key_html, unsafe_allow_html=True)

# Display feedback message
if st.session_state.feedback_message:
    st.markdown(f"<h3 style='color:{st.session_state.feedback_color};'>{st.session_state.feedback_message}</h3>", unsafe_allow_html=True)

# Manual refresh button for the note score
if st.button("Refresh Note Score"):
    # Refresh the current key and reset the feedback message
    st.session_state.current_key = random.choice(list(KEY_SCORES.keys()))
    st.session_state.feedback_message = ""

#st.markdown("## Write anything you want below the piano here.")
#st.write("This is where you can add any text, charts, or other content you want to display below the piano visualization.")
