import streamlit as st
import soundfile as sf
from pathlib import Path
import base64
import random
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# Add custom CSS to reduce the white space without cropping the text
st.markdown("""
    <style>
    /* Reduce the space above the content without cropping the title */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    .stApp {
        margin-top: 0px;  /* Remove the negative margin */
    }
    </style>
    """, unsafe_allow_html=True)

# Define the notes and their corresponding files
NOTE_FILES = {
    'C6': 'notes/c6.wav',
    'C#6': 'notes/c_sharp_6.wav',
    'D6': 'notes/d6.wav',
    'D#6': 'notes/d_sharp_6.wav',
    'E6': 'notes/e6.wav',
    'F6': 'notes/f6.wav',
    # 'F#6': 'notes/f_sharp_6.wav',
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
    # 'F#6': 'key_scores/f_sharp_6.png',
    'G6': 'key_scores/g6.png',
    'G#6': 'key_scores/g_sharp_6.png',
    'A6': 'key_scores/a6.png',
    'A#6': 'key_scores/a_sharp_6.png',
    'B6': 'key_scores/b6.png',
}

# Function to get a random image and its corresponding key
def get_random_image():
    return random.choice(list(KEY_SCORES.items()))

# Initialize session state for random image and feedback message
if 'random_image' not in st.session_state:
    st.session_state.random_key, st.session_state.random_image = get_random_image()

if 'feedback_message' not in st.session_state:
    st.session_state.feedback_message = ""

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
        var keyElement = document.getElementById('{note}');
        keyElement.classList.add('pressed');
        setTimeout(function() {{
            keyElement.classList.remove('pressed');
        }}, 2000);
        </script>
        """
        components.html(audio_html, height=0, width=0)
    else:
        pass

# Styling keys to resemble piano keys with a 60% height ratio for black keys
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
        transition: transform 0.1s ease;
    }
    .white-key.pressed {
        background-color: lightgray;
        transform: translateY(5px);
        border-top: none;  /* Completely remove the top border when pressed */
    }
    .white-key .label {
        position: absolute;
        bottom: 5px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 14px;
        color: black;
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
        height: 120px;  /* 60% of the height of white keys */
        display: inline-block;
        position: absolute;
        margin-left: -20px;
        z-index: 3;  /* Ensure black key stays on top */
        top: 0;
        transition: transform 0.1s ease;
    }
    .black-key.pressed {
        background-color: darkgray;
        transform: translateY(5px);
        border-top-color: darkgray;  /* Hide the top border when pressed */
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
            label = 'C4' if key_name == 'C4' else ''
            keys_layout.append((key_name, style, is_active, label))
    return keys_layout

# Define the layout for the keys (Octaves 4, 5, 6)
keys_layout = generate_keys_layout(octave_range=range(4, 7), active_octave=6)

# Get the random image and its associated key from session state
random_key = st.session_state.random_key
random_image = st.session_state.random_image

# Function to check if the pressed key matches the displayed key
def check_key_press(note):
    if note == random_key:
        st.session_state.feedback_message = "Correct!"
        st.session_state.feedback_color = "green"
    else:
        st.session_state.feedback_message = "Incorrect"
        st.session_state.feedback_color = "red"

# Render the keys horizontally
st.title("Score Sync App / Igor Wilk / August 2024")
st.image(random_image, use_column_width=False)
columns = st.columns(len(keys_layout))

for i, (note, style, is_active, label) in enumerate(keys_layout):
    with columns[i]:
        if is_active:
            if st.button("▶", key=note):
                play_note_and_animate(note)
                check_key_press(note)
        else:
            st.button("▶", key=note, disabled=True)
        
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
    st.session_state.random_key, st.session_state.random_image = get_random_image()
    st.session_state.feedback_message = ""
    # No need for experimental rerun, we manually refresh state and UI elements

#st.markdown("## Write anything you want below the piano here.")
#st.write("This is where you can add any text, charts, or other content you want to display below the piano visualization.")
