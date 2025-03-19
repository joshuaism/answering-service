import os

# constants for sending/recieving emailed transcript files
SENDER_GMAIL = os.environ.get("GMAIL_ACCT")
SENDER_GMAIL_PASSWORD = os.environ.get("GMAIL_APP_PW")
RECIPIENT_EMAIL = 'riffeljobsearch@gmail.com'

# constant for chrome user account (for selenium to access google voice)
# should look something like C:\Users\<your user>\AppData\Local\Google\Chrome\User Data\ in windows
CHROME_DATA_DIRECTORY = os.environ.get('CHROME_USER_DATA_PATH')

# constants for setting the input and output devices the answering service script will listen and output to
# a list of your system devices can be found by running service\devices.py
INPUT_DEVICE = "Stereo Mix (Realtek(R) Audio)"
OUTPUT_DEVICE = "CABLE Input (VB-Audio Virtual Cable)"

# constants for your personal information used by the answering service script
FIRST_NAME = "Josh"
LAST_NAME = "Riffel"
NEAREST_METRO = "Houston"
CITY = "Friendswood"
STATE = "Texas"

# constant to query distance from job location to {CITY} {STATE} in the answering service script
# set your api key from https://www.wolframalpha.com/
WOLFRAM_ALPHA_API_KEY = os.environ.get('WOLFRAM_ALPHA_API_KEY')

# constant for acceptable commute distances in miles
ONSITE_COMMUTE = 30
HYBRID_COMMUTE = 50
