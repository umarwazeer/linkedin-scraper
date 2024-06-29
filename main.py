import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from client import LIClient
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

def parse_command_line_args():
    parser = argparse.ArgumentParser(description="Parse LinkedIn search parameters")
    parser.add_argument('--username', type=str, required=True, help="Enter LI username")
    parser.add_argument('--password', type=str, required=True, help="Enter LI password")
    parser.add_argument('--keyword', type=str, nargs='*', help="Enter search keys")
    parser.add_argument('--location', type=str, nargs='*', help="Enter search locations")
    parser.add_argument('--sort_by', type=str, default='Relevance', help="Sort by relevance or date posted")
    return vars(parser.parse_args())

def initialize_driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def login_with_retry(driver, liclient):
    max_attempts = 3
    current_attempt = 1
    while current_attempt <= max_attempts:
        try:
            liclient.login()
            return  # Exit function if login is successful
        except Exception as e:
            print(f"Attempt {current_attempt} failed. Error: {e}")
            if "502 Bad Gateway" in str(e):
                print("Encountered 502 Bad Gateway. Retrying in 5 seconds...")
                time.sleep(5)
            current_attempt += 1
    print("Failed to login after multiple attempts.")

if __name__ == "__main__":
    search_keys = parse_command_line_args()

    driver = initialize_driver()
    liclient = LIClient(driver, **search_keys)

    try:
        login_with_retry(driver, liclient)
        liclient.search_jobs()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if driver:
            driver.quit()

