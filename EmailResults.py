from email.message import EmailMessage
import win32com.client as win32
import subprocess
import smtplib
import json
import logging
import os
import time


def sendEmail(removed_songs):
    return removed_songs != []


def generateBody(removed_songs):
    body = ""

    for playlist in removed_songs:
        youtubePrefix = "www.youtube.com/watch?v="
        for name in playlist:
            for song in playlist[name]:
                body += (
                    name + " - " + song[0] + " - " + youtubePrefix + song[1] + "\r\n"
                )

    return body


def emailError(error_msg, ex):
    email_json = open("data.json")
    email_data = json.load(email_json)

    outlook = win32.Dispatch("outlook.application")
    mail = outlook.CreateItem(0)
    mail.To = email_data["to-email"]
    mail.Subject = error_msg
    mail.Body = str(ex)

    mail.Send()
    os.system("taskkill /im outlook.exe /f")

    # with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    #     msg = EmailMessage()
    #     msg["Subject"] = error_msg
    #     msg["From"] = email_data["from-email"]["email"]
    #     msg["To"] = email_data["to-email"]
    #     msg.set_content(str(ex))

    #     try:
    #         smtp.login(email_data["from-email"]["email"], email_data["from-email"]["password"])
    #     except Exception:
    #         logging.exception("Failed to login to email")

    #     try:
    #         smtp.send_message(msg)
    #     except Exception:
    #         logging.exception("Failed to send email")


def removedSongsAmount(removed_songs):
    amount = 0
    for playlist in removed_songs:
        for name in playlist:
            amount += len(playlist[name])
    return amount


def is_outlook_running():
    try:
        temp = subprocess.check_output("tasklist", shell=True)
        return "OUTLOOK.EXE" in str(temp)
    except Exception:
        return False


def emailResults(removed_songs):
    attempts = 0
    max_attempts = 5
    while not is_outlook_running():
        if attempts < max_attempts:
            subprocess.Popen(
                r"C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE"
            )
            time.sleep(10)
            attempts += 1
        else:
            emailError(f"Failed to start Outlook after {max_attempts} attempts.", ":(")
            return

    email_json = open("data.json")
    email_data = json.load(email_json)

    outlook = win32.Dispatch("outlook.application")
    mail = outlook.CreateItem(0)
    mail.To = email_data["to-email"]
    mail.Subject = str(removedSongsAmount(removed_songs)) + " Removed Songs"
    mail.Body = generateBody(removed_songs)

    mail.Send()
    time.sleep(30)
    os.system("taskkill /im outlook.exe /f")

    # with smtplib.SMTP_SSL("smtp.gmail.com", 587) as smtp:
    #     msg = EmailMessage()
    #     msg["Subject"] = str(removedSongsAmount(removed_songs)) + " Removed Songs"
    #     msg["From"] = email_data["from-email"]["email"]
    #     msg["To"] = email_data["to-email"]
    #     msg.set_content(generateBody(removed_songs))

    #     try:
    #         smtp.login(email_data["from-email"]["email"], email_data["from-email"]["password"])
    #     except Exception:
    #         logging.exception("Failed to login to email")

    #     try:
    #         smtp.send_message(msg)
    #     except Exception:
    #         logging.exception("Failed to send email")
