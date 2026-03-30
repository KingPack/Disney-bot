import json
import random
from typing import Dict, List, Optional
from urllib.parse import quote_plus

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from app.bot.browser import build_browser
from app.bot.behavior import HumanBehavior
from app.bot.parser import ProfileParser

LOGIN_URL = "https://www.linkedin.com/login"
BASE_SEARCH_URL = "https://www.linkedin.com/search/results/people/?origin=GLOBAL_SEARCH_HEADER"


class LinkedInBot:
    def __init__(self, headless: bool = True, timeout: int = 20):
        self.driver: Chrome = build_browser(headless=headless)
        self.timeout = timeout
        self.logged_in = False

    def _wait(self, locator, timeout: Optional[int] = None):
        return WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.presence_of_element_located(locator)
        )

    def login(self, username: str, password: str) -> bool:
        self.driver.get(LOGIN_URL)
        self._wait((By.ID, "username"))
        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.url_contains("/feed")
            )
            self.logged_in = True
            return True
        except TimeoutException:
            if self.driver.find_elements(By.XPATH, "//input[@placeholder='Search']"):
                self.logged_in = True
                return True
            raise RuntimeError("LinkedIn login failed. Verify credentials and account status.")

    def load_cookies(self, cookies: List[Dict]) -> bool:
        self.driver.get("https://www.linkedin.com")
        cookie_list = cookies
        if isinstance(cookies, str):
            cookie_list = json.loads(cookies)

        for cookie in cookie_list:
            cookie_data = dict(cookie)
            cookie_data.pop("sameSite", None)
            if "expiry" in cookie_data and isinstance(cookie_data["expiry"], str):
                try:
                    cookie_data["expiry"] = int(cookie_data["expiry"])
                except ValueError:
                    cookie_data.pop("expiry", None)
            try:
                self.driver.add_cookie(cookie_data)
            except Exception:
                continue

        self.driver.refresh()
        return self.check_logged_in()

    def check_logged_in(self, timeout: Optional[int] = None) -> bool:
        self.driver.get("https://www.linkedin.com/feed")
        try:
            self._wait((By.XPATH, "//input[@placeholder='Search']"), timeout=timeout or 10)
            self.logged_in = True
            return True
        except TimeoutException:
            self.logged_in = False
            return False

    def get_cookies(self) -> List[Dict]:
        return self.driver.get_cookies()

    def search_recruiters(
        self,
        query: str = "recruiter",
        location: Optional[str] = None,
        limit: int = 20,
    ) -> List[Dict[str, str]]:
        if not self.logged_in:
            raise RuntimeError("Bot must be logged in before searching.")

        search_query = quote_plus(query)
        search_url = f"{BASE_SEARCH_URL}&keywords={search_query}"
        if location:
            search_url += f"&location={quote_plus(location)}"

        self.driver.get(search_url)
        self._wait((By.CSS_SELECTOR, "div.search-results__cluster-content-wrapper, ul.reusable-search__entity-result-list"))
        HumanBehavior.scroll(self.driver, depth=2)
        HumanBehavior.random_delay(0.8, 1.6)

        candidates = []
        cards = self.driver.find_elements(By.CSS_SELECTOR, "div.search-result__wrapper, div.entity-result__item")

        for card in cards:
            if len(candidates) >= limit:
                break

            text = card.text
            parsed = ProfileParser.parse_profile(text)
            if not parsed.get("is_recruiter"):
                continue

            try:
                name = card.find_element(By.XPATH, ".//span[contains(@class,'actor-name')] | .//span[contains(@class,'name actor-name')] | .//a[contains(@href, '/in/')]/span").text.strip()
            except NoSuchElementException:
                name = "Unknown"

            try:
                link = card.find_element(By.XPATH, ".//a[contains(@href, '/in/')]").get_attribute("href").split("?")[0]
            except NoSuchElementException:
                link = ""

            candidates.append({"name": name, "url": link})

        return candidates

    def connect_recruiters(self, limit: int = 5) -> List[Dict[str, str]]:
        if not self.logged_in:
            raise RuntimeError("Bot must be logged in before connecting.")

        connected = []
        cards = self.driver.find_elements(By.CSS_SELECTOR, "div.search-result__wrapper, div.entity-result__item")

        for card in cards:
            if len(connected) >= limit:
                break

            try:
                button = card.find_element(
                    By.XPATH,
                    ".//button[normalize-space()='Connect' or contains(@aria-label, 'Connect') or contains(text(), 'Connect')]",
                )
            except NoSuchElementException:
                continue

            if not button.is_displayed():
                continue

            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", button)
            HumanBehavior.random_delay(1.0, 2.0)

            try:
                button.click()
            except ElementClickInterceptedException:
                continue

            self._confirm_connect_modal()
            name = card.text.split("\n")[0].strip() or "Unknown"
            url = ""
            try:
                url = card.find_element(By.XPATH, ".//a[contains(@href, '/in/')]").get_attribute("href").split("?")[0]
            except NoSuchElementException:
                pass

            connected.append({"name": name, "url": url})
            HumanBehavior.random_delay(1.5, 3.0)

        return connected

    def _confirm_connect_modal(self) -> None:
        try:
            send_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[.//span[text()='Send now'] or .//span[text()='Send']]")
                )
            )
            send_button.click()
        except TimeoutException:
            pass

    def close(self) -> None:
        self.driver.quit()
