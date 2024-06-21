import os
import time

import yaml
from dotenv import load_dotenv
from selenium.common.exceptions import (StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from setup import Setup


def get_google_credentials():
    load_dotenv()
    email = os.getenv("GOOGLE_EMAIL")
    password = os.getenv("GOOGLE_PASSWORD")
    if not email or not password:
        raise ValueError("Google email and password must be set in the environment variables")
    return email, password


with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)
    DEFAULT_RETRY_ATTEMPTS = config['DEFAULT_RETRY_ATTEMPTS']
    DEFAULT_WAIT = config['DEFAULT_WAIT_TIME']


class BedrockSolver:
    def __init__(self, driver, email, password, wait_time=DEFAULT_WAIT, retry_attempts=DEFAULT_RETRY_ATTEMPTS):
        self.driver = driver
        self.wait = WebDriverWait(driver, wait_time)
        self.email = email
        self.password = password
        self.retry_attempts = retry_attempts

    def wait_for_visibility(self, locator):
        for _ in range(self.retry_attempts):
            try:
                return self.wait.until(EC.presence_of_element_located(locator))
            except Exception as e:
                print(f"Exception finding visibility of {locator}, refreshing page. {e!r}")
                self.driver.refresh()
                continue
            else:
                raise RuntimeError("Attempts exhausted to find visibility")

    def wait_for_clickability(self, locator):
        for _ in range(self.retry_attempts):
            try:
                return self.wait.until(EC.element_to_be_clickable(locator))
            except Exception as e:
                print(f"Exception finding clickability of {locator}, refreshing page. {e!r}")
                self.driver.refresh()
                continue
            else:
                raise RuntimeError("Attempts exhausted to find clickability")

    def sign_in(self):
        self.driver.get("https://app.bedrocklearning.org/")
        self.wait_for_clickability((By.CLASS_NAME, "btn--google")).click()
        self.wait_for_clickability((By.CSS_SELECTOR, "input[type='email']")).send_keys(self.email)
        self.wait_for_clickability((By.XPATH, "//button[contains(.,'Next')]")).click()
        self.wait_for_clickability((By.CSS_SELECTOR, "input[type='password']")).send_keys(self.password)
        self.wait_for_clickability((By.XPATH, "//button[contains(.,'Next')]")).click()

    def select_task(self):
        try:
            all_buttons = solver.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.btn")))
            vocab_button = all_buttons[1].click()
        except Exception as e:
            time.sleep(2)
            print(f"Faced exception trying to click vocabulary button. Retrying. {e}")
            all_buttons = solver.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.btn")))
            vocab_button = all_buttons[1].click()


email, password = get_google_credentials()
setup = Setup()
driver = setup.get_chromedriver()

solver = BedrockSolver(driver, email, password)
solver.sign_in()
solver.select_task()
input()
driver.quit()
