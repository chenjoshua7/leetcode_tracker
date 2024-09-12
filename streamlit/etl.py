import pandas as pd
import pymysql

class ETL:
    def __init__(self) -> None:
        self.df = None
        
        self.retrieve_data()
        pass
    
    def retrieve_data(self):
        import pymysql
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="huahua20101",
            db="leetcode"
        )
        try:
            cursor = connection.cursor()

            # Execute query to fetch data from daily_problems
            cursor.execute("SELECT * FROM daily_problems ORDER BY prob_date DESC")
            self.df = pd.DataFrame(cursor.fetchall())
            
        finally:
            cursor.close()
            connection.close()

    def clean_data(self):
        columns = ["id","date","name","acceptance","complexity","complete_time","skills","notes","gpt","completed","speed","memory"]
        self.df.columns = columns
        
        self.df['day'] = self.df['date'].dt.date  # Extract just the date (YYYY-MM-DD)
        self.df['time'] = self.df['date'].dt.time
    
    def export(self):
        return self.df
    
class DataQuerier:
    def __init__(self) -> None:
        self.connection = None
        self.col_names = None
        self._connect()
        self._get_column_names()
        pass
    
    def _connect(self):
        endpoint = "leetcode.c9eq4wc6mqs0.us-east-2.rds.amazonaws.com"
        port = 3306
        username = "admin"
        password = "Huahua2010!"
        database = "leetcode"

        try:
            self.connection = pymysql.connect(
                host=endpoint,
                user=username,
                password=password,
                database=database,
                port=port
            )
            print("Connection successful!")
            
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
    
    def _get_column_names(self):
        self.col_names = list(self.query("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'daily_problems'")[0])
    
    def query(self, query, *args, **kwargs):
        column_names = kwargs.get("columns_names", None) or kwargs.get("col_names", None) or kwargs.get("columns", None) 
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                print("Successfully Executed")
                if column_names:
                    return pd.DataFrame(results, columns = column_names)
                else:
                    return pd.DataFrame(results)
        except pymysql.MySQLError as e:
            print(f"Error: {e}")