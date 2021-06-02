#!/usr/bin/python3

import sys
import smtplib
from time import sleep

sender = 'alertemailsamjakes@gmail.com'
receiver = 'sampcjakes@gmail.com'
queryDelay = 1
batteryThreshold = 10
alertSent = False

# Define the message including sender and receiver
preMessage = """From: Battery Alert <{}>
To: Battery Manager <{}>
Subject: Battery is below {}%

This is an automated email to notify you that the battery level has fallen below {}%.
"""
message = preMessage.format(sender, receiver, str(batteryThreshold), str(batteryThreshold))


try:
    while True:
        
        with open('batteryLevel.txt', 'r') as batteryFile:
            
            # Read battery percentage file
            lines = batteryFile.readlines()
            if len(lines) < 1:
                continue

            # If an alert has already been sent
            if alertSent:

                # Don't send an alert if the battery is still low
                if int(lines[-1]) <= batteryThreshold + 10:
                    print("Battery hasn't been fixed...")
                    sleep(queryDelay)
                    continue
                
                # If the battery has been recharged by a significant amount, reset
                if int(lines[-1]) > batteryThreshold + 10:
                    print("Recharge detected, alert reset")
                    alertSent = False
                    sleep(queryDelay)
                    continue

                
            if int(lines[-1]) <= batteryThreshold:
                print("Battery level fell below threshold!")
                smtpObj = smtplib.SMTP_SSL('smtp.gmail.com', 465 )
                smtpObj.ehlo()
                smtpObj.login('alertemailsamjakes@gmail.com', 'alertgardenhosesam')
                smtpObj.sendmail(sender, receiver, message)
                alertSent = True
                print("Successfully sent email alert")
        sleep(queryDelay)

except smtplib.SMTPException as err:
    print("Error: unable to send email")
    print(err)
except KeyboardInterrupt:
    batteryFile.close()

batteryFile.close()