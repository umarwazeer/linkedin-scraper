import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from client import LIClient
from settings import search_keys
import time


chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("user-agent=whatever you want")
# chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--incognito")

def parse_command_line_args():
    parser = argparse.ArgumentParser(description="Parse LinkedIn search parameters")
    parser.add_argument('--username', type=str, required=True, help="Enter LinkedIn username")
    parser.add_argument('--password', type=str, required=True, help="Enter LinkedIn password")
    parser.add_argument('--keyword', default=search_keys['keywords'], nargs='*', help="Enter search keys separated by a single space")
    parser.add_argument('--location', default=search_keys['locations'], nargs='*', help="Enter search locations separated by a single space")
    parser.add_argument('--search_radius', type=int, default=search_keys['search_radius'], nargs='?', help="Enter a search radius (in miles)")
    parser.add_argument('--results_page', type=int, default=search_keys['page_number'], nargs='?', help="Enter a specific results page")
    parser.add_argument('--date_range', type=str, default=search_keys['date_range'], nargs='?', help="Specify a specific date range")
    parser.add_argument('--sort_by', type=str, default=search_keys['sort_by'], nargs='?', help="Sort results by relevance or date posted")
    parser.add_argument('--salary_range', type=str, default=search_keys['salary_range'], nargs='?', help="Set a minimum salary requirement")
    parser.add_argument('--filename', type=str, default=search_keys['filename'], nargs='?', help="Specify a filename to which data will be written")
    return vars(parser.parse_args())

if __name__ == "__main__":
    search_keys = parse_command_line_args()

    # Initialize Selenium WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print(chrome_options, service, )

    # Initialize LinkedIn web client
    print(search_keys)
    liclient = LIClient(driver, **search_keys)

    try:
        liclient.login()

        # Wait for page load
        time.sleep(3)

        assert isinstance(search_keys["keyword"], list)
        assert isinstance(search_keys["location"], list)

        for keyword in search_keys["keyword"]:
            for location in search_keys["location"]:
                liclient.keyword = keyword
                liclient.location = location
                # Additional methods for navigating and searching jobs
                liclient.search_jobs()

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if liclient.driver:
            liclient.driver.quit()
