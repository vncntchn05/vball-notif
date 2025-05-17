import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
disable_warnings(InsecureRequestWarning)

import requests
from bs4 import BeautifulSoup
import re

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from datetime import datetime
import time

def time_string_to_int(time_str: str) -> int:
    """
    Converts a time string like '8:30 PM' to an integer like 2030.
    
    Args:
        time_str (str): Time in format like '8:30 PM'
        
    Returns:
        int: Time as integer in HHMM 24-hour format, e.g., 8:30 PM → 2030
    """
    dt = datetime.strptime(time_str.strip(), "%I:%M %p")
    return dt.hour * 100 + dt.minute


def click_button_by_date(page, date: datetime):
    # Format the datetime to match "May 21, 2025"
    formatted_date = date.strftime("%B %-d, %Y")  # On Linux/macOS
    # For Windows, use: formatted_date = date.strftime("%B %#d, %Y")

    # Wait for and click the button
    # mobile button?
    page.locator(f'button.single-date-select-one-click[data-date-text="{formatted_date}"]').click()


def is_spot_available(target_date: datetime, target_start_time: str, max_retries: int = 3) -> bool:
    """
    Checks if spots are available for a specific SERVE volleyball session.
    
    Args:
        target_date: datetime object of the session date
        target_start_time: string of start time (e.g., "3:01 PM")
    
    Returns:
        bool: True if spots are available, False otherwise
    """
    with sync_playwright() as p:
        for attempt in range(max_retries):
            try:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()

                # Navigate to program page
                url = "https://warrior.uwaterloo.ca/program/GetProgramDetails?courseId=2882ad00-6e10-4b25-ac28-238a716ab8c5"
                page.goto(url, timeout=15000)
                
                # Wait for calendar to load (more specific selector)
                page.wait_for_selector("div.program-instance-card", timeout=10000)
                
                click_button_by_date(page, target_date)
                print("hi")

                # Add slight delay for stability
                time.sleep(1)
                
                # Find matching session
                cards = page.query_selector_all("div.program-instance-card")
                for card in cards:
                    try:
                        time_element = card.query_selector(".instance-time-header")
                        if not time_element:
                            continue
                            
                        time_text = time_element.inner_text()
                        start_time = time_text.split(" - ")[0].strip().split("\n")[1]
                        
                        if start_time.lower() == target_start_time.lower():
                            spots_element = card.query_selector(".spots-tag")
                            if not spots_element:
                                return False
                                
                            availability = spots_element.inner_text().lower()
                            print(availability)

                            if "no spots" in availability:
                                return False
                            elif any(char.isdigit() for char in availability):
                                return True
                            return False
                    
                    except Exception as e:
                        print(f"Error parsing card: {e}")
                        continue
                
                raise ValueError(f"No session found at {target_start_time} on {target_date.strftime('%Y-%m-%d')}")
                
            except PlaywrightTimeoutError:
                if attempt == max_retries - 1:
                    print("Max retries reached, giving up")
                    return False
                print(f"Timeout occurred, retrying ({attempt + 1}/{max_retries})")
                continue
                
            except Exception as e:
                print(f"Error checking availability: {e}")
                return False
                
            finally:
                if browser:
                    browser.close()
        
        return False

# Example usage
if __name__ == "__main__":
    # Check if spots available for April 4, 2025 at 3:01 PM, datetime(year, month, day)
    date = datetime(2025, 5, 21)
    start_time = "8:30 PM"
    
    if is_spot_available(date, start_time):
        print(f"Spots available for {start_time} on {date.strftime('%Y-%m-%d')}!")
    else:
        print(f"No spots available for {start_time} on {date.strftime('%Y-%m-%d')}")

    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = "classesuwaterloobot@gmail.com"
    receiver_email = "vncntchn05@gmail.com"
    password = "lxtikuxorkjzcmqf"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Serve Spot Update"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = ""

    part1 = MIMEText(text, "plain")

    message.attach(part1)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

'''
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
        if int(datalist[wanti + 4]) > int(datalist[wanti + 5]):
            return True, "There is an open spot for " + subject + " " + cournum + " (" + classnum + ")"
        return False, ""
    return False, ""
'''

