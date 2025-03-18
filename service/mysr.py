import speech_recognition as sr

speech = sr.Recognizer()


def get_device_index(input_device):
    index = 0
    for device in sr.Microphone.list_microphone_names():
        if device == input_device:
            return index
        else:
            index = index + 1
    return -1


def voice_to_text(input_device=None, language='en-US', timeout=None):
    voice_input = ""
    input_index = 0
    if input_device:
        input_index = get_device_index(input_device)
    # 0: Microsoft Sound Mapper - Input
    # 1: Microphone Array (Realtek(R) Au
    # 2: Stereo Mix (Realtek(R) Audio)
    # Use Stereo Mix to record speaker output (may need to enable in windows settings > sound > recording)
    mic = sr.Microphone(device_index=input_index)
    with mic as source:
        speech.adjust_for_ambient_noise(source)
        print(f'''python is listening on device {input_index} 
            {sr.Microphone.list_microphone_names()[input_index]} 
            using {language} speech recognition''')
        try:
            audio = speech.listen(source, timeout=timeout)
            voice_input = speech.recognize_google(audio, language=language)
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            pass
        except sr.WaitTimeoutError:
            pass
    return voice_input
