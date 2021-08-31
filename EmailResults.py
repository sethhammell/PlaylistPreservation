from email.message import EmailMessage
import smtplib
import json
import logging

def sendEmail(removed_songs):
    return removed_songs != []

def generateBody(removed_songs):
    body = ""

    for playlist in removed_songs:
        for name in playlist:
            for song in playlist[name]:
                body += name + " - " + song + '\r\n'
    
    return body

def emailError(error_msg, ex):
    email_json = open("data.json")
    email_data = json.load(email_json)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        msg = EmailMessage()
        msg["Subject"] = error_msg
        msg["From"] = email_data["from-email"]["email"]
        msg["To"] = email_data["to-email"]
        msg.set_content(str(ex))

        try:
            smtp.login(email_data["from-email"]["email"], email_data["from-email"]["password"])
        except Exception:
            logging.exception("Failed to login to email")
        
        try:
            smtp.send_message(msg)
        except Exception:
            logging.exception("Failed to send email")
        
def removedSongsAmount(removed_songs):
    amount = 0
    for playlist in removed_songs:
        for name in playlist:
            amount += len(playlist[name])
    return amount

def emailResults(removed_songs):
    email_json = open("data.json")
    email_data = json.load(email_json)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        msg = EmailMessage()
        msg["Subject"] = str(removedSongsAmount(removed_songs)) + " Removed Songs"
        msg["From"] = email_data["from-email"]["email"]
        msg["To"] = email_data["to-email"]
        msg.set_content(generateBody(removed_songs))

        try:
            smtp.login(email_data["from-email"]["email"], email_data["from-email"]["password"])
        except Exception:
            logging.exception("Failed to login to email")
        
        try:
            smtp.send_message(msg)
        except Exception:
            logging.exception("Failed to send email")
