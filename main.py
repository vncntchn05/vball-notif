import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
disable_warnings(InsecureRequestWarning)

import requests
from bs4 import BeautifulSoup
import re


def spotcheck(level, sess, subject, cournum, classnum):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'level': level,
        'sess': sess,
        'subject': subject,
        'cournum': cournum,
    }

    response = requests.post('https://classes.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl', headers=headers, data=data, verify=False)

    if response != None:
        html = "" + response.text

        soup = BeautifulSoup(html, 'html.parser')

        datalist = []

        for data in soup.find_all('td'):
            if data.string is not None:
                t = re.sub('[^0-9a-zA-Z]+', '', data.string)
                if t != '':
                    datalist.append(t)

        wanti = datalist.index(classnum)
        if int(datalist[wanti + 5]) > int(datalist[wanti + 6]):
            return True, "There is an open spot for " + subject + " " + cournum + " (" + classnum + ")"
        return False, ""
    return False, ""

def spotcheck2(level, sess, subject, cournum, classnum):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'level': level,
        'sess': sess,
        'subject': subject,
        'cournum': cournum,
    }

    response = requests.post('https://classes.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl', headers=headers, data=data, verify=False)

    if response != None:
        html = "" + response.text

        soup = BeautifulSoup(html, 'html.parser')

        datalist = []

        for data in soup.find_all('td'):
            if data.string is not None:
                t = re.sub('[^0-9a-zA-Z]+', '', data.string)
                if t != '':
                    datalist.append(t)

        wanti = datalist.index(classnum)
        #print(int(datalist[wanti + 6]) + int(datalist[wanti + 10]) - int(datalist[wanti + 11]))
        if int(datalist[wanti + 5]) > int(datalist[wanti + 6]) + int(datalist[wanti + 10]) - int(datalist[wanti + 11]):
            return True, "There is an open spot for " + subject + " " + cournum + " (" + classnum + ")"
        return False, ""
    return False, ""

def spotcheck3(level, sess, subject, cournum, classnum):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'level': level,
        'sess': sess,
        'subject': subject,
        'cournum': cournum,
    }

    response = requests.post('https://classes.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl', headers=headers, data=data, verify=False)

    if response != None:
        html = "" + response.text

        soup = BeautifulSoup(html, 'html.parser')

        datalist = []

        for data in soup.find_all('td'):
            if data.string is not None:
                t = re.sub('[^0-9a-zA-Z]+', '', data.string)
                if t != '':
                    datalist.append(t)

        wanti = datalist.index(classnum)
        #print(int(datalist[wanti + 7]) + int(datalist[wanti + 11]) - int(datalist[wanti + 12]))
        if int(datalist[wanti + 6]) > int(datalist[wanti + 7]) + int(datalist[wanti + 11]) - int(datalist[wanti + 12]):
            return True, "There is an open spot for " + subject + " " + cournum + " (" + classnum + ")"
        return False, ""
    return False, ""

def spotcheck4(level, sess, subject, cournum, classnum):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'level': level,
        'sess': sess,
        'subject': subject,
        'cournum': cournum,
    }

    response = requests.post('https://classes.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl', headers=headers, data=data, verify=False)

    if response != None:
        html = "" + response.text

        soup = BeautifulSoup(html, 'html.parser')

        datalist = []

        for data in soup.find_all('td'):
            if data.string is not None:
                t = re.sub('[^0-9a-zA-Z]+', '', data.string)
                if t != '':
                    datalist.append(t)

        wanti = datalist.index(classnum)
        print(datalist)
        if int(datalist[wanti + 4]) > int(datalist[wanti + 5]):
            return True, "There is an open spot for " + subject + " " + cournum + " (" + classnum + ")"
        return False, ""
    return False, ""

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
sess = "1245"
subject = "MATH"
cournum = "239"
classnum = "3761"

p = spotcheck(level, sess, subject, cournum, classnum)[0]
q = spotcheck(level, sess, subject, cournum, "3762")[0]
r = spotcheck2(level, sess, subject, cournum, "3868")[0]
s = spotcheck3(level, sess, subject, cournum, "3887")[0]
t1 = spotcheck4(level, sess, subject, cournum, "3767")[0]
t2 = spotcheck4(level, sess, subject, cournum, "3869")[0]

if p and (t1 or t2):
    text = spotcheck(level, sess, subject, cournum, classnum)[1]

    part1 = MIMEText(text, "plain")

    message.attach(part1)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
if q and (t1 or t2):
    text = spotcheck(level, sess, subject, cournum, "3762")[1]

    part1 = MIMEText(text, "plain")

    message.attach(part1)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
if r and (t1 or t2):
    text = spotcheck2(level, sess, subject, cournum, "3868")[1]

    part1 = MIMEText(text, "plain")

    message.attach(part1)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
if s and (t1 or t2):
    text = spotcheck3(level, sess, subject, cournum, "3887")[1]

    part1 = MIMEText(text, "plain")

    message.attach(part1)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())