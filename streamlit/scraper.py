import streamlit as st
import pymysql
from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from sidebar import sidebar

# Web scraping class
class LeetCodeDailyScraper:
    def __init__(self) -> None:
        pass

    def run(self):
        url = "https://leetcode.com/problemset/"
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        chrome_options.add_argument("--disable-gpu")  # Disable GPU usage
        chrome_options.add_argument("--no-sandbox")  # Required for some environments
        chrome_options.add_argument("--disable-dev-shm-usage")
        
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
        return daily_problem

# Helper class to acquire information
class GetInformation:
    def __init__(self, daily_problem) -> None:
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

# SQL Loader
def load_into_sql(info):
    endpoint = "leetcode.c9eq4wc6mqs0.us-east-2.rds.amazonaws.com"
    port = 3306
    username = "admin"
    password = "Huahua2010!"
    database = "leetcode"

    try:
        connection = pymysql.connect(
            host=endpoint,
            user=username,
            password=password,
            database=database,
            port=port
        )

        with connection.cursor() as cursor:
            try:
                cursor.execute("""
                    INSERT INTO daily_problems 
                    (id, date, name, complexity, acceptance_rate, time, language, speed, memory, chat_gpt, skills, notes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (info.id, info.start_time, info.name, info.complexity, info.acceptance_rate, info.time, info.language, 
                     info.speed, info.memory, info.gpt, info.skills, info.notes)
                )
                connection.commit()
            except pymysql.MySQLError as e:
                st.error(f"Error inserting data: {e}")
    except pymysql.MySQLError as e:
        st.error(f"Connection Error: {e}")
    finally:
        connection.close()

# Streamlit App
def scraper_page():
    sidebar()
    st.title("LeetCode Daily Problem Scraper")

    if "start_time" not in st.session_state:
        st.session_state.start_time = None
    if "stop_time" not in st.session_state:
        st.session_state.stop_time = None
    if "daily_problem" not in st.session_state:
        st.session_state.daily_problem = None

    # Scrape today's problem
    if st.button("Scrape Today's Problem"):
        scraper = LeetCodeDailyScraper()
        st.session_state.daily_problem = scraper.run()

    # Display the scraped problem info if available
    if st.session_state.daily_problem:
        daily_problem = st.session_state.daily_problem
        st.write(f"**Problem ID**: {daily_problem[0]}")
        st.write(f"**Problem Name**: {daily_problem[1]}")
        st.write(f"**Acceptance Rate**: {daily_problem[2]}")
        st.write(f"**Complexity**: {daily_problem[3]}")

        # Start the timer if not already started
        if st.session_state.start_time is None:
            if st.button("Start Timer"):
                st.session_state.start_time = time.time()

    # Show stop button if timer has started
    if st.session_state.start_time and st.session_state.stop_time is None:
        if st.button("Stop Timer"):
            st.session_state.stop_time = time.time()

    # After stopping the timer, display the fields for entering additional info
    if st.session_state.stop_time:
        elapsed_time = st.session_state.stop_time - st.session_state.start_time
        st.write(f"Time taken: {elapsed_time:.2f} seconds")

        # Input fields for additional info
        speed = st.number_input('Input Speed (in ms):', min_value=0.0, step=1.0)
        memory = st.number_input('Input Memory (in MB):', min_value=0.0, step=1.0)
        gpt_used = st.checkbox("Did you use ChatGPT?")
        skills = st.text_input("Enter the skills used (comma separated):")
        notes = st.text_area("Enter any notes:", "")

        # Submit button to save the data to the database
        if st.button("Submit Data"):
            info = GetInformation(st.session_state.daily_problem)
            info.time = elapsed_time
            info.speed = speed
            info.memory = memory
            info.gpt = 1 if gpt_used else 0
            info.skills = skills
            info.notes = notes
            info.start_time = datetime.fromtimestamp(st.session_state.start_time).strftime('%Y-%m-%d %H:%M:%S')

            # Load data into SQL
            load_into_sql(info)
            st.success("Data loaded successfully into SQL.")
            
            # Reset session state after submission
            st.session_state.start_time = None
            st.session_state.stop_time = None
            st.session_state.daily_problem = None

if __name__ == '__main__':
    scraper()
