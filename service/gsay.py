from io import BytesIO
from gtts import gTTS
from pygame import mixer, time


def print_say(text, lang='en-US', halt=True, output=None):
    """Uses the gTTS engine to generate speech from text
    Parameters:
    text (str): the text to output
    language (str): the language to speak
    halt (bool): blocks the thread until the speech is complete
    """
    tts = gTTS(text, lang=lang)
    print(text)
    voice = BytesIO()
    tts.write_to_fp(voice)
    voice.seek(0)
    mixer.init(devicename=output)
    mixer.music.load(voice)
    mixer.music.play()
    if halt:
        while mixer.music.get_busy():
            time.Clock().tick(10)
