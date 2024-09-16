import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

# Webscraping Daily Problem Info from LeetCode
class LeetCodeDailyScraper:
    def __init__(self) -> None:
        pass

    def run(self):
        url = "https://leetcode.com/problemset/"
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(url)

        soup = self._get_soup(driver)
        scraped_data = self._scrape_main_page(soup)

        driver.quit()

        return scraped_data

    def _get_soup(self, driver):
        time.sleep(2)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        return soup

    def _scrape_main_page(self, soup: BeautifulSoup) -> list:
        daily_problem = soup.find("a", href=True, class_="h-5 hover:text-blue-s dark:hover:text-dark-blue-s")
        daily_problem = daily_problem.contents[0].split(". ")

        row = soup.find_all("div", attrs={"role": "row"})[1].contents
        daily_problem.append(float(row[3].contents[0].contents[0][:-1]))
        daily_problem.append(row[4].contents[0].contents[0])
        print(daily_problem)
        return daily_problem

# acquires information to submit
class GetInformation:
    def __init__(self) -> None:
        scraper = LeetCodeDailyScraper()
        daily_problem = scraper.run()

        self.id = daily_problem[0]
        self.name = daily_problem[1]
        self.acceptance_rate = daily_problem[2]
        self.complexity = daily_problem[3]
        self.language = "Python"

        self.time = None
        self.speed = None
        self.memory = None
        self.gpt = None
        self.skills = []
        self.notes = None
        self.start_time = None

    def run(self):
        self._problem_time()
        self._stats()
        self._language()
        self._chat_gpt()
        self._get_skills()  # Ensure this is called to get skills
        self._get_notes()
        self.skills = ", ".join(skill for skill in self.skills)

    def _problem_time(self):
        start = time.time()
        self.start_time = datetime.fromtimestamp(start).strftime('%Y-%m-%d %H:%M:%S')
        pausetime = 0

        while True:
            finished = input('Type "done" when finished (Type "pause" to pause): ').lower()

            if finished == "pause":
                pausetime += time.time() - start
                input("Hit Enter to resume timer")
                start = time.time()  # Restart the timer after resuming

            elif finished == "done":
                end = time.time()
                self.time = end - start + pausetime
                break

        # Verification loop
        while True:
            verify = input(f"Enter 0 if time is incorrect - {self.time} seconds\nVerify: ")
            if verify == "0":
                try:
                    actual_time = float(input("Enter your actual time (in seconds): "))
                    self.time = actual_time
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid time in seconds.")
            else:
                break

    def _language(self):
        language = input("Enter Language (default Python): ")
        if language:
            self.language = language.capitalize()

    def _stats(self):
        while True:
            try:
                self.speed = float(input("Input Speed: "))
                self.memory = float(input("Input Memory: "))
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def _chat_gpt(self):
        chatgpt = input("Enter 1 if ChatGPT was used: ")
        if chatgpt == "1":
            self.gpt = 1
        else:
            self.gpt = 0

    def _get_skills(self):
        while True:
            skill = input("Input skills (if completed, press Enter): ")
            if not skill:
                break
            else:
                self.skills.append(skill)

    def _get_notes(self):
        while True:
            notes = input("Type any notes: ")
            if len(notes) > 255:
                print("Too many characters, maximum 255")
            else:
                self.notes = notes
                break
