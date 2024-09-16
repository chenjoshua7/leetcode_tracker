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
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
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
    st.write("")
    st.markdown("<h2 style='text-align: center; padding-bottom: 10px;'>LeetCode Daily Problem Scraper</h2>", unsafe_allow_html = True)

    # Scrape today's problem
    if st.button("Start Today's Problem") and not st.session_state.finished:
        scraper = LeetCodeDailyScraper()
        st.session_state.daily_problem = scraper.run()
    

    st.markdown("""This functionality is not supported on Streamlit Cloud due to the lack of Selenium support, but it works seamlessly when run locally, as demonstrated in the video below. This limitation is acceptable since the application is designed for personal use, and I prefer to keep my database private.
                For those interested in setting this up for personal use, the GitHub repository is linked in the sidebar. You can begin by following the steps in the `AWS_setup` Jupyter Notebook.
                The error shown in the video occurs because I have already completed today's daily problem.
                """)
    st.video("example.mov")
    
    if "start_time" not in st.session_state:
        st.session_state.start_time = None
    if "stop_time" not in st.session_state:
        st.session_state.stop_time = None
    if "paused_time" not in st.session_state:
        st.session_state.paused_time = None
    if "elapsed_time" not in st.session_state:
        st.session_state.elapsed_time = 0
    if "daily_problem" not in st.session_state:
        st.session_state.daily_problem = None
    if "finished" not in st.session_state:
        st.session_state.finished = False
    if "timer_active" not in st.session_state:
        st.session_state.timer_active = False

            
            
    # Display the scraped problem info if available
    if st.session_state.daily_problem:
        space1, c1, c2, c3, space2 = st.columns([0.01, 0.3, 0.2, 0.2, 0.5])
        daily_problem = st.session_state.daily_problem
        c1.write(f"{daily_problem[0]}. {daily_problem[1]}")
        c2.write(f"Acceptance: {daily_problem[2]}%")
        c3.write(f"Complexity: {daily_problem[3]}")
        
        st.session_state.start_time = time.time() - st.session_state.elapsed_time
        st.session_state.timer_active = True

    # Timer controls: Start, Pause, Stop
    placeholder = st.empty()

    # Continuously update elapsed time if timer is running
    if st.session_state.timer_active and st.session_state.start_time:
        st.session_state.elapsed_time = time.time() - st.session_state.start_time
        placeholder.write(f"Elapsed time: {st.session_state.elapsed_time:.2f} seconds")
    elif st.session_state.finished:
        placeholder.write(f"Final time: {st.session_state.elapsed_time:.2f} seconds")  # Keep showing final time after stop

    # Stop button logic
    if st.session_state.daily_problem:
        if st.button("Stop Timer") and not st.session_state.finished:
            if st.session_state.start_time:
                st.session_state.stop_time = time.time()
                st.session_state.elapsed_time = st.session_state.stop_time - st.session_state.start_time
                st.session_state.timer_active = False
                st.session_state.finished = True
                placeholder.write(f"Final time: {st.session_state.elapsed_time:.2f} seconds")  # Show final time after stopping

        # Continuously update elapsed time if timer is running
        if st.session_state.start_time and st.session_state.paused_time is None and not st.session_state.finished:
            while st.session_state.timer_active:
                st.session_state.elapsed_time = time.time() - st.session_state.start_time
                placeholder.write(f"Elapsed time: {st.session_state.elapsed_time:.2f} seconds")
                time.sleep(0.01)
        else:
            placeholder.write(f"Final time: {st.session_state.elapsed_time:.2f} seconds")

    if st.session_state.finished:
        space, input_data, space2 = st.columns([0.3, 1, 0.3])

        speed = input_data.number_input('Input Speed (in %):', min_value=0.0, step=1.0)
        memory = input_data.number_input('Input Memory (in %):', min_value=0.0, step=1.0)
        gpt_used = input_data.checkbox("Did you use ChatGPT?")
        skills = input_data.text_input("Enter the skills used (comma separated):")
        notes = input_data.text_area("Enter any notes:", "")

        # Submit button to save the data to the database
        if input_data.button("Submit Data"):
            info = GetInformation(st.session_state.daily_problem)
            info.time = st.session_state.elapsed_time
            info.speed = speed
            info.memory = memory
            info.gpt = 1 if gpt_used else 0
            info.skills = skills
            info.notes = notes
            info.start_time = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

            # Load data into SQL
            load_into_sql(info)
            input_data.success("Data loaded successfully into SQL.")

            # Reset session state after submission
            st.session_state.start_time = None
            st.session_state.stop_time = None
            st.session_state.paused_time = None
            st.session_state.daily_problem = None
            st.session_state.finished = False  # Reset the finished state

if __name__ == '__main__':
    scraper_page()
