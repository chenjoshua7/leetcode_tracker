import time
import json
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager




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


def problem_time():
    start = time.time()
    pausetime = 0
    while True:
        finished = input('Type "done" when finished (Type "pause" to pause"):' )
        if finished.lower() == "pause":
            pausetime += time.time() - start
            input("Hit Enter to resume timer")
            start = time.time()
        
        elif finished.lower() == "done":
            end = time.time()
            break
    return end - start + pausetime

def get_skills():
    skills = []
    while True:
        skill = input("Input skills (if completed, press Enter): ")
        if not skill:
            break
        else:
            skills.append(skill)
    return skills

def get_notes():
    notes = input("Type any notes: ")
    if len(notes) > 255:
        notes = get_notes()
    return notes

def accepted():
    accept = input("Enter 1 if Accepted: ")
    if accept == "1":
        print("good job")
        return 1
    else:
        return 0

def ChatGPT():
    chatgpt = input("Enter 1 if ChatGPT: ")
    if chatgpt == "1":
        return 1
    else:
        return 0

def stats():
    speed = input("Input Speed: ")
    memory = input("Input Memory: ")
    return speed, memory

def load_into_sql(daily_problem, completion_time, accepted, chat_gpt, skills, notes, speed, memory):
    import pymysql
    conn = pymysql.connect(host='localhost',
                        user='root',
                        password='huahua20101',
                        db='leetcode')

    cursor = conn.cursor()
    
    skills = ", ".join(skill for skill in skills)

    # Insert data into the daily_problems table
    cursor.execute("""
        INSERT INTO daily_problems (problem_id, prob_name, accpetance, complexity, accepted, chat_gpt, completion_time, skills, speed, memory, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (daily_problem[0], daily_problem[1], daily_problem[2], daily_problem[3], accepted, chat_gpt, completion_time, skills, speed, memory, notes)
    )

    # Commit the transaction
    conn.commit()
    conn.close()
    
def load_data():
    retries = 3
    attempt = 0
    while attempt < retries:
        try:
            accept = accepted()
            gpt = ChatGPT()
            skills = get_skills()
            speed, memory = stats()
            notes = get_notes()

            # Attempt to load the data into SQL
            load_into_sql(daily_problem, completion_time, accept, gpt, skills, notes, speed, memory)
            print("Data loaded successfully into SQL.")
            break  # Exit loop on successful load
        
        except Exception as e:
            attempt += 1
            print(f"Error loading data (attempt {attempt}): {e}")

            if attempt == retries:
                print("Max retries reached. Data could not be loaded.")

if __name__== '__main__':
    scraper = LeetCodeDailyScraper()
    daily_problem = scraper.run()
    completion_time = problem_time()
    load_data()
    print("Data Successfuly Loaded.")