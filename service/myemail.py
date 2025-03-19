import smtplib
from email.message import EmailMessage
from constants import SENDER_GMAIL, SENDER_GMAIL_PASSWORD

from mysr import voice_to_text
from mysay import print_say


def email(file=None, recipient=None, subline=None, content=None):
    # Build a dictionary of names and emails
    # Different email providers have different domain name and port number
    mysmt = smtplib.SMTP('smtp.gmail.com', 587)
    mysmt.ehlo()
    mysmt.starttls()
    # Use your own login info; you may need an app password
    mysmt.login(SENDER_GMAIL, SENDER_GMAIL_PASSWORD)

    # Send the actual email
    msg = EmailMessage()
    msg['Subject'] = subline
    msg['From'] = SENDER_GMAIL
    msg['To'] = recipient
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
