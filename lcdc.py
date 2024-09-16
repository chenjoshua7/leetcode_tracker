import pymysql
from helper_objects import GetInformation

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
            except pymysql.MySQLError as e:
                print(f"Error inserting data: {e}")
            connection.commit()

    except pymysql.MySQLError as e:
        print(f"Connection Error: {e}")
    
    finally:
        connection.close()


## Tries to load the entry three times
def load_data(info):
    retries = 3
    attempt = 0
    while attempt < retries:
        try:
            load_into_sql(info)
            print("Data loaded successfully into SQL.")
            break
        except Exception as e:
            attempt += 1
            print(f"Error loading data (attempt {attempt}): {e}")

            if attempt == retries:
                print("Max retries reached. Data could not be loaded.")


if __name__ == '__main__':
    info = GetInformation()
    info.run()
    load_data(info)
    print("Data successfully loaded.")
