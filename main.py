import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

UW_USERNAME = os.getenv("UW_USERNAME")
UW_PASSWORD = os.getenv("UW_PASSWORD")

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
disable_warnings(InsecureRequestWarning)

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from datetime import datetime
import time

def login_to_warrior(page, username: str, password: str) -> bool:
    """
    Logs into the Warrior Recreation website.
    
    Args:
        page: Playwright page object
        username: Your UW username
        password: Your UW password
    
    Returns:
        bool: True if login successful, False otherwise
    """
    try:
        page.goto("https://warrior.uwaterloo.ca", timeout=10000)
        login_button = page.locator('button#loginLinkBtn.TopBarButtonColor.LoginPartialLinks.btn.btn-link')

        if login_button.count() > 0:
            # Go to login page
            login_button.click()
            page.locator('button.btn-sign-in[title="WATIAM USERS"]').click()

            # Fill and submit login form
            page.fill('#userNameInput', username)
            page.locator('#nextButton.submit.nextButton').click()
            page.fill("#passwordInput", password)
            page.locator('#submitButton.submit.modifiedSignIn').click()
            
            # Wait for login to complete (check for a post-login element)
            page.wait_for_selector('span.Menu-IconName:has-text("Club Memberships and Sessions")', timeout=5000)
            return True
        
    except Exception as e:
        print(f"Login failed: {e}")
        return False

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
    formatted_date = date.strftime("%B %d, %Y").replace(" 0", " ")
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

                login_to_warrior(page, UW_USERNAME, UW_PASSWORD)
                
                # Navigate to program page
                url = "https://warrior.uwaterloo.ca/program/GetProgramDetails?courseId=2882ad00-6e10-4b25-ac28-238a716ab8c5"
                page.goto(url, timeout=15000)
                # Wait for calendar to load (more specific selector)
                page.wait_for_selector("div.program-instance-card", timeout=10000)
                
                click_button_by_date(page, target_date)
                
                # Add slight delay for stability
                time.sleep(1)
                
                # page.screenshot(path="screenshot.png", full_page=True)

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
    date = datetime(2025, 11, 4)
    start_time = "9:30 PM"
    send = True
    
    if is_spot_available(date, start_time):
        print(f"Spots available for {start_time} on {date.strftime('%Y-%m-%d')}!")
        if send:
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

    else:
        print(f"No spots available for {start_time} on {date.strftime('%Y-%m-%d')}")
