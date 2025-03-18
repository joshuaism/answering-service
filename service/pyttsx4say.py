import pyttsx4
from pygame import mixer, time
from io import BytesIO

engine = pyttsx4.init()
voices = engine.getProperty('voices')
# for voice in voices:
#    print(voice)
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 180)


def __set_language__(language='en-US'):
    if language == 'ja':
        # you'll need to install japanese support in windows
        # check the properties on your machine to find the index for Haruka
        engine.setProperty('voice', voices[2].id)
        engine.setProperty('rate', 125)
    else:
        engine.setProperty('voice', voices[1].id)
        engine.setProperty('rate', 180)


def print_say(text, language='en-US', halt=True, output=None):
    """Uses the pyttsx4 engine to generate speech from text
    Parameters:
    text (str): the text to output
    language (str): the language to speak
    halt (bool): blocks the thread until the speech is complete
    """
    __set_language__(language)
    print(text)
    b = BytesIO()
    engine.save_to_file(text, b)
    engine.runAndWait()
    # the bs is raw data of the audio.
    bs = b.getvalue()
    # add an wav file format header
    b = bytes(b'RIFF') + (len(bs)+38).to_bytes(4, byteorder='little')+b'WAVEfmt\x20\x12\x00\x00' \
        b'\x00\x01\x00\x01\x00' \
        b'\x22\x56\x00\x00\x44\xac\x00\x00' +\
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
