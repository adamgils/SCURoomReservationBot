from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import schedule

load_dotenv()


def book_room():
    # Set Booking Date
    six_days = timedelta(days=6)
    booking_date = datetime.today() + six_days
    booking_date_str = booking_date.strftime("%m/%d/%Y")

    # Initialize Driver
    PATH = "/Users/adamgilani/PycharmProjects/SCURoomResBot/chromedriver"

    service = Service(PATH)
    service.start()
    driver = webdriver.Remote(service.service_url)
    driver.implicitly_wait(30)

    driver.get("https://www.scu.edu/apps/rooms/")

    # Input Username from .env
    username = os.getenv("USERNAME")
    uname = driver.find_element("id", "username")
    uname.send_keys(username)

    # Input Password from .env
    password = os.getenv("PASSWORD")
    pword = driver.find_element("id", "password")
    pword.send_keys(password)

    # Click Login
    driver.find_element("name", "_eventId_proceed").click()

    # Click Grid View
    grid = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.LINK_TEXT, "Grid")
        )
    )
    grid.click()

    # Click on LC 210
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.LINK_TEXT, "LC 210")
        )
    )
    element.click()

    # Click Other Date
    other = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.LINK_TEXT, "Other...")
        )
    )
    other.click()

    # Input Date
    date_input = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.ID, "dpr_startdate")
        )
    )
    date_input.clear()
    date_input.send_keys(booking_date_str)

    # Check what day of the week it is
    date_num = booking_date.weekday()
    weekday = [0, 1, 2, 3, 4]

    if date_num in weekday:
        # Input Start Time at 8am
        time_text = "8:00 AM"
        time_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "time_start"))
        )
        time_input.clear()
        time_input.send_keys(time_text)
    else:
        # Input Start Time at 11am
        time_text = "11:00 AM"
        time_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "time_start"))
        )
        time_input.clear()
        time_input.send_keys(time_text)

    # Input Event Name
    event_text = "Room Reservation"
    event_input = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "purpose"))
    )
    event_input.send_keys(event_text)

    # Click Hours Amount
    if date_num in weekday:
        hours_button = driver.find_element(By.LINK_TEXT, "2 hrs")
        hours_button.click()
        time.sleep(5)
    else:
        hours_button = driver.find_element(By.LINK_TEXT, "4 hrs")
        hours_button.click()
        time.sleep(5)

    # Click Done
    done_button = driver.find_element(By.CLASS_NAME, "btn-success")
    done_button.click()
    time.sleep(5)

    # Click Done Again
    done_button = driver.find_element(By.CLASS_NAME, "btn")
    done_button.click()
    time.sleep(5)

    time.sleep(5)
    driver.quit()


book_room()
