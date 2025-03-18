import pygame
import pygame._sdl2.audio as sdl2_audio
import speech_recognition as sr


pygame.mixer.init()
devices = tuple(sdl2_audio.get_audio_device_names(False))
pygame.mixer.quit()
# voice_to_text()
print("\n\noutput devices")
for device in devices:
    print(device)

devices = sr.Microphone.list_microphone_names()

print("\ninput devices")
for device in devices:
    print(device)
