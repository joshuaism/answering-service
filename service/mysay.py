import gsay
import pyttsx4say


def print_say(text, language='en-US', engine="pyttsx4", halt=True, output=None):
    """Uses the specified engine to generate speech from text
    Parameters:
    text (str): the text to output
    language (str): the language to speak
    halt (bool): blocks the thread until the speech is complete
    output (str): sets the audio output device
    """
    if engine.lower() == "gtts":
        gsay.print_say(text, lang=language, halt=halt, output=output)
    else:
        pyttsx4say.print_say(text, language=language, halt=halt, output=output)
