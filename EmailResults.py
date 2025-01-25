import json
import logging
import os
import smtplib
from email.message import EmailMessage

def sendEmail(removed_songs):
    return removed_songs != []

def generateBody(removed_songs):
    body = ""
    youtubePrefix = "www.youtube.com/watch?v="
    for playlist in removed_songs:
        for name in playlist:
            for song in playlist[name]:
                body += f"{name} - {song[0]} - {youtubePrefix}{song[1]}\r\n"
    return body

def removedSongsAmount(removed_songs):
    amount = 0
    for playlist in removed_songs:
        for name in playlist:
            amount += len(playlist[name])
    return amount

def send_smtp_email(subject, body, email_data):
    """
    Send an email using SMTP (e.g. Gmail SMTP).
    email_data dict should contain:
       - email_data["from-email"]["email"]
       - email_data["from-email"]["password"]
       - email_data["to-email"]
    """
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = email_data["from-email"]["email"]
    msg["To"] = email_data["to-email"]
    msg.set_content(body)

    try:
        # Connect to Gmail's SMTP server (port 465 with SSL, or port 587 with STARTTLS)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(
                email_data["from-email"]["email"], 
                email_data["from-email"]["password"]
            )
            smtp.send_message(msg)
        print(f"Email successfully sent to {email_data['to-email']}.")
    except Exception as e:
        logging.exception("Failed to send email via SMTP")
        raise e

def emailError(error_msg, ex):
    """Send an email for errors."""
    with open("data.json") as email_json:
        email_data = json.load(email_json)

    subject = error_msg
    body = str(ex)

    # Send via SMTP
    send_smtp_email(subject, body, email_data)

def emailResults(removed_songs):
    """Send an email with the list of removed songs."""
    with open("data.json") as email_json:
        email_data = json.load(email_json)

    subject = f"{removedSongsAmount(removed_songs)} Removed Songs"
    body = generateBody(removed_songs)

    # Send via SMTP
    send_smtp_email(subject, body, email_data)

