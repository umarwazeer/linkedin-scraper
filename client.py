import os
import pickle
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class LIClient:
    def __init__(self, driver, **kwargs):
        self.driver = driver
        self.kwargs = kwargs
        self.cookies_file = "linkedin_cookies.pkl"

    def save_cookies(self):
        with open(self.cookies_file, "wb") as file:
            pickle.dump(self.driver.get_cookies(), file)

    def load_cookies(self):
        if os.path.exists(self.cookies_file):
            with open(self.cookies_file, "rb") as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
            return True
        return False

    def login(self):
        self.driver.get("https://www.linkedin.com/login")

        # Attempt to load cookies if they exist
        if self.load_cookies():
            self.driver.get("https://www.linkedin.com/feed/")
            time.sleep(5)  # Wait for the page to load
            if "feed" in self.driver.current_url:
                print("Logged in using cookies.")
                return
            else:
                print("Cookies expired or invalid. Proceeding with login.")

        email_input = self.driver.find_element(By.ID, "username")
        password_input = self.driver.find_element(By.ID, "password")

        email_input.send_keys(self.kwargs.get('username'))
        time.sleep(2)  # Wait to mimic human behavior
        password_input.send_keys(self.kwargs.get('password'))
        time.sleep(2)  # Wait to mimic human behavior
        password_input.send_keys(Keys.RETURN)

        time.sleep(5)  # Wait for the page to load

        if "Security Verification" in self.driver.title:
            print("Security verification required. Please complete the CAPTCHA manually.")
            input("Press Enter after completing the CAPTCHA...")  # Wait for user to complete CAPTCHA
            while "Security Verification" in self.driver.title:
                time.sleep(5)  # Wait until security verification is completed

        if "Your noCAPTCHA user response code is missing or invalid." in self.driver.page_source:
            raise Exception("CAPTCHA response is missing or invalid.")

        if "Wrong email or password" in self.driver.page_source:
            raise Exception("Login failed: Wrong email or password.")

        print("Logged in successfully. Current page title: ", self.driver.title)
        self.save_cookies()

    def search_jobs(self):
        # Implementation of job search logic
        pass  # Replace with your job search implementation

