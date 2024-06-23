from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

class LIClient:
    def __init__(self, driver, **kwargs):
        self.driver = driver
        self.kwargs = kwargs

    def login(self):
        self.driver.get("https://www.linkedin.com/login")

        email_input = self.driver.find_element(By.ID, "username")
        password_input = self.driver.find_element(By.ID, "password")

        email_input.send_keys(self.kwargs.get('username'))
        time.sleep(2)  # Wait to mimic human behavior
        password_input.send_keys(self.kwargs.get('password'))
        time.sleep(2)  # Wait to mimic human behavior
        password_input.send_keys(Keys.RETURN)

        time.sleep(5)  # Wait for the page to load
        print(self.driver.title)
        # Check if CAPTCHA challenge is present
        if "Security Verification" in self.driver.title:
            print("Security verification required. Please complete the CAPTCHA manually.")
            input("Press Enter after completing the CAPTCHA...")  # Wait for user to complete CAPTCHA
            print(self.driver.title, self.driver.page_source)
            while "Security Verification" in self.driver.title:
                print("waiting for",)
                time.sleep(5)  # Wait until security verification is completed
            print("after captua", self.driver.page_source, self.driver.title )        

        # Check if login was successful
        if "Your noCAPTCHA user response code is missing or invalid." in self.driver.page_source:
            raise Exception("CAPTCHA response is missing or invalid.")

        print("Logged in successfully. Current page title: ", self.driver.title)

    def search_jobs(self):
        # Implementation of job search logic
        pass  # Replace with your job search implementation


if __name__ == "__main__":
    # Example usage
    username = "umarkhan580830@gmail.com"
    password = "u4umarkhan@580830"

    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("user-agent=whatever you want")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--incognito")

    driver = webdriver.Chrome(options=chrome_options)
    liclient = LIClient(driver, username=username, password=password)

    try:
        liclient.login()
        # Proceed with other operations like job search
        liclient.search_jobs()

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if driver:
            driver.quit()
