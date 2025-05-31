import json
import pyttsx4
from pygame import mixer, time
from io import BytesIO
import inflect
import re

engine = pyttsx4.init('coqui_ai_tts')
engine.setProperty('speaker_wav', './files/take2.wav')
inflect_engine = inflect.engine()

with open('files/coqui.json', 'r') as content:
    pronounciations = json.load(content)


def fix_pronounciations(text: str):
    new_text = text
    numbers = re.findall(r'\d+', text)
    for number in numbers:
        new_text = new_text.replace(
            number, inflect_engine.number_to_words(int(number)), 1)
    for key in pronounciations.keys():
        text = text.replace(key, f"{key}*")
        new_text = new_text.replace(key, pronounciations.get(key))

    return new_text, text


def print_say(text: str, language='en-US', halt=True, output=None):
    """Uses the coqui.ai model to generate speech from text
    Parameters:
    text (str): the text to output
    language (str): the language to speak
    halt (bool): blocks the thread until the speech is complete
    """
    new_text, text = fix_pronounciations(text)
    print(text)
    b = BytesIO()
    engine.save_to_file(new_text, b)
    engine.runAndWait()
    # the bs is raw data of the audio.
    bs = b.getvalue()
    # add an wav file format header
    b = bytes(b'RIFF') + (len(bs)+38).to_bytes(4, byteorder='little')+b'WAVEfmt\x20\x12\x00\x00' \
        b'\x00\x01\x00\x01\x00' \
        b'\x22\x3e\x00\x00\x44\xac\x00\x00' +\
        b'\x02\x00\x10\x00\x00\x00data' + \
        (len(bs)).to_bytes(4, byteorder='little')+bs
    # changed to BytesIO
    b = BytesIO(b)
    mixer.init(devicename=output)
    mixer.music.load(b)
    mixer.music.play()
    if (halt):
        while mixer.music.get_busy():
            time.Clock().tick(10)
