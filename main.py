import smtplib, ssl
from helper import spotcheck
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
disable_warnings(InsecureRequestWarning)

port = 465
smtp_server = "smtp.gmail.com"

# optional input prompts
# reciever_email = input("Type your email and press enter: ")
# password = input("Type your password and press enter: ")
                                                                                                  #full           open
# level = input("Level of study (under/grad): ")                                                  #under          under
# sess = input("Term (1231=Winter 2023, 1235=Spring 2023, 1239=Fall 2023, 1241=Winter 2024): ")   #1239           1239
# subject = input("Subject code: ")                                                               #MATH           MATH
# cournum = input("Course number: ")                                                              #145            145
# classnum = input("Class number: ")                                                              #6025           6506

sender_email = "classesuwaterloobot@gmail.com"
receiver_email = "vncntchn05@gmail.com"
password = "lxtikuxorkjzcmqf"

message = MIMEMultipart("alternative")
message["Subject"] = "Spot Update"
message["From"] = sender_email
message["To"] = receiver_email

level = "under"
sess = "1239"
subject = "MATH"
cournum = "145"
classnum = "6025"

p = spotcheck(level, sess, subject, cournum, classnum)[0]

if p:
    text = spotcheck(level, sess, subject, cournum, classnum)[1]

    part1 = MIMEText(text, "plain")

    message.attach(part1)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    print("sent email, " + text)

