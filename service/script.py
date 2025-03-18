import os
import random
import time
import json
import wolframalpha
from mysay import print_say
from mysr import voice_to_text

INPUT_DEVICE = "Stereo Mix (Realtek(R) Audio)"
OUTPUT_DEVICE = "CABLE Input (VB-Audio Virtual Cable)"
APIkey = os.environ.get('WOLFRAM_ALPHA_API_KEY')
wolf = wolframalpha.Client(APIkey)

# Open phone.json and put it in a dictionary
with open('files/phone.json', 'r') as content:
    chats = json.load(content)


def contains(str, strings):
    for string in strings:
        if string in str:
            return True
    return False


def print_say_write(str, file=None, halt=True):
    if file:
        file.write(f"assistant: {str}\n")
    print_say(str, halt=halt, output=OUTPUT_DEVICE)


def get_input(file=None, caller="caller"):
    count = 0
    inp = ""
    while count < 3:
        inp = voice_to_file(file, caller)
        if inp == "":
            count = count + 1
        else:
            break
    return inp


def voice_to_file(file=None, caller="caller"):
    # inp = input("ready")
    # inp = voice_to_text()
    inp = voice_to_text(input_device=INPUT_DEVICE)
    if file:
        file.write(f"{caller}: {inp}\n")
    return inp.lower()


def process_tokens(inp, file=None):
    tokens = inp.split(' ')
    token_captured = False
    if 'space city games' in inp:
        token_captured = True
        print_say_write("You mentioned space city games", file=file)
        print_say_write(random.choice(chats['space city games']), file=file)
    for key in chats.keys():
        if key in tokens:
            token_captured = True
            print_say_write(f"You mentioned {key}", file=file)
            print_say_write(random.choice(chats[key]), file=file)
    if not token_captured:
        print_say_write(f"You asked {inp},", file=file)
        print_say_write(random.choice(chats["_confused"]), file=file)
        print_say_write(random.choice(chats["_recover"]), file=file)


def run_script(caller):
    file = open("file.txt", "w", encoding='utf8')
    file.write(f"Answered call from {caller}\n")
    print_say_write("""Hello, this is the Josh Riffel Job Bot.
        This conversation is being transcribed and your responses will be forwarded to Josh Riffel.
        If you do not consent to having this conversation recorded, or this is not about a new job or role,
        please hang up now.""")
    print_say_write("Before we start", file=file)
    print_say_write(
        "Name a few skills Josh will use in this new role.", file=file, halt=False)
    inp = get_input(file, caller)
    if inp == "":
        print_say_write(
            "I didn't hear any response so I'm leaving the conversation, goodbye!", file=file)
        return
    else:
        if contains(inp, chats["initialize_conv"]):
            print_say_write(random.choice(chats["initialize_resp"]), file=file)
        else:
            process_tokens(inp, file=file)

    time.sleep(.5)

    print_say_write("""Hopefully I've been able to demonstrate some of my ability to you.
        Josh wrote this service in python in the hope it would save all of us a little bit of time.
        So let's get to this real quick.""", file=file)

    print_say_write(
        "First off, Who are you and what company do you represent?", file=file)
    inp = get_input(file, caller)
    print_say_write(random.choice(chats["_acknowledged"]), file=file)

    print_say_write(
        "Josh is currently working remote and resides near Houston Texas", file=file)
    print_say_write("Is this a remote, hybrid, or onsite role?",
                    file=file, halt=False)

    remote = False
    inp = get_input(file, caller)
    if "remote" in inp:
        remote = True
        print_say_write("That's great to hear! But regardless", file=file)
    print_say_write("What city is the role located in?", file=file, halt=False)
    inp = get_input(file, caller)
    if "houston" not in inp:
        response = wolf.query(f"how far is {inp} from friendswood texas")
        try:
            ans = next(response.results).text
            print(ans)
            distance = round(float(ans.replace(' miles', '')))
            if remote:
                print_say_write(
                    f"So that's about {distance} miles from his current location.  Good to know.", file=file)
            else:
                if distance < 30:
                    print_say_write("That is probably doable", file=file)
                elif distance < 50:
                    print_say_write(
                        f"That's at least {distance} miles away, but as long as it's not five days a week it might work",
                        file=file)
                else:
                    print_say_write(f"""That's at least {distance} miles away! 
                        Josh can't relocate at this time so this is not very promising news.""",
                                    file=file)
        except (ValueError, StopIteration):
            print_say_write(
                "I don't know where that is but maybe Josh will look into it.", file=file)
    else:
        print_say_write(
            "That might work but will depend on what side of Houston it's on.", file=file)

    print_say_write("Is this a full time or contract role",
                    file=file, halt=False)
    inp = get_input(file, caller)
    if "contract" in inp:
        print_say_write(
            "Not ideal, Josh might have some questions about this later", file=file)
    else:
        print_say_write(random.choice(chats["_acknowledged"]), file=file)

    print_say_write("What is the pay rate for this role?",
                    file=file, halt=False)
    inp = get_input(file, caller)
    print_say_write(random.choice(chats["_acknowledged"]), file=file)

    print_say_write(
        "Is there anything else you want Josh to know about this opportunity?", file=file, halt=False)
    inp = get_input(file, caller)
    print_say_write(random.choice(chats["_acknowledged"]), file=file)

    print_say_write(
        "Well that's it for my questions. I've noted your responses and will send them to Josh.", file=file)
    print_say_write(
        "You are free to ask me anything about Josh's work history now and I will answer to the best of my ability",
        file=file)

    finished = False
    while not finished:
        print_say_write(random.choice(chats["_ask"]), file=file, halt=False)
        inp = get_input(file, caller)
        if inp == "":
            print_say_write(
                "I didn't hear any questions so I'm leaving the conversation", file=file)
            return
        else:
            if contains(inp, chats["_stop"]) or inp == "no":
                finished = True
            elif contains(inp, chats["initialize_conv"]):
                print_say_write(random.choice(
                    chats["initialize_resp"]), file=file)
            else:
                process_tokens(inp, file)

    print_say_write(
        "If you have no more questions then, do you have any parting thoughts?", file=file)
    print_say_write(
        "Maybe want to tell me how you would rate this experience?", file=file, halt=False)
    inp = get_input(file, caller)
    print_say_write(random.choice(chats["_acknowledged"]), file=file)
    print_say_write("""And with that I would like to thank you for your time."
        Have a great rest of your day.  Goodbye!""", file=file)


if __name__ == '__main__':
    print("starting")
    INPUT_DEVICE = None
    OUTPUT_DEVICE = None
    run_script("local test")
