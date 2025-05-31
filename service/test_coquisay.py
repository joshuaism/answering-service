import json
from mysay import print_say

print_say("hi mom")
print_say("hi mom", engine="pyttsx4")
print_say("hello world")
print_say("hello world", engine="gtts")
# TODO: find a way to handle japanese with coqui
print_say("おはようございます。")

with open('files/experience.json', 'r') as content:
    experiences = json.load(content)

for key in experiences:
    print_say(f"You mentioned {key}. {experiences.get(key)}")

while True:
    inp = input("What do you want to convert to speech?\n")
    if inp == "done":
        print_say(f"You just typed in done; goodby!")
        break
    else:
        print_say(inp)
