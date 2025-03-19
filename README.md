# answering-service

An app for running an answering service on google voice for handling recruiter calls. The app transcribes the audio from all calls and emails the transcripts of each conversation to you.

# Install

Create a virtual environment

```commandline
python -m venv env
```

Install requirements

```commandline
pip install -r requirements.txt
```

# Prerequisites to run the application

You will need to install chrome, set up a google account, set that google account as the user profile for chrome, and set up google voice for that user profile

Next update constants.py with your personal information and system settings

Then, in google voice, click the headphone icon to set your microphone to match your OUTPUT_DEVICE and speakers to match your INPUT_DEVICE settings in constants.py

![image](https://github.com/user-attachments/assets/7982975a-ae9d-4fba-9b16-88b7150ec39e)

(It is highly recommended to download a virtual audio device so you can have separate audio streams for input and output to prevent feedback/crosstalk)


# Run

Enter your environment (in windows)

```commandline
env\scripts\activate
```

Run the app

```commandline
python service\google_voice.py
```
