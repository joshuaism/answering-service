import smtplib
import os
import csv
from email.message import EmailMessage

from mysr import voice_to_text
from mysay import print_say

gmail_acct = os.environ.get("GMAIL_ACCT")
gmail_app_pw = os.environ.get("GMAIL_APP_PW")

# Define the email() function


def email(file=None, name=None, subline=None, content=None):
    # Build a dictionary of names and emails
    emails = {}
    with open('files/emails.csv') as data:
        for line in csv.DictReader(data, skipinitialspace=True):
            emails[line['name']] = line['email']
    # Different email providers have different domain name and port number
    mysmt = smtplib.SMTP('smtp.gmail.com', 587)
    mysmt.ehlo()
    mysmt.starttls()
    # Use your own login info; you may need an app password
    mysmt.login(gmail_acct, gmail_app_pw)
    # Voice input the name of the recipient
    if not name:
        print_say('Who do you want to send the email to?', halt=False)
        name = voice_to_text().lower()
        print_say(f"You just said {name}.")
    email = emails[name]
    # Voice input the subject line
    if not subline:
        print_say('What is the subject line?', halt=False)
        subline = voice_to_text()
        print_say(f"You just said {subline}.")
    # Voice input the email content
    if not content:
        print_say('What is the email content?', halt=False)
        content = voice_to_text()
        print_say(f"You just said {content}.")
    # Send the actual email
    msg = EmailMessage()
    msg['Subject'] = subline
    msg['From'] = gmail_acct
    msg['To'] = email
    msg.set_content(content)
    if file:
        msg.add_attachment(
            open(file, "rb").read(),
            maintype='text',
            subtype='plain',
            filename=file
        )
    mysmt.send_message(msg)
    print_say('Ok, email sent.')
    mysmt.quit()
