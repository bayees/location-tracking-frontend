from dotenv import load_dotenv
import sqlalchemy as sa
import pandas as pd
import os

load_dotenv()

SQL_CONNECTION_STRING = sa.engine.URL.create(
        "mssql+pyodbc",
        username=os.getenv('DATABASE_USER'),
        password=os.getenv('DATABASE_PASSWORD'),
        host=os.getenv('DATABASE_HOST'),
        database="warehouse",
        query={
            "driver": "ODBC Driver 17 for SQL Server",
        },
    )
engine = sa.create_engine(SQL_CONNECTION_STRING)

def load_data():
    
    df = pd.read_sql('SELECT * FROM dash.positions', engine)
    df['date_actual'] = pd.to_datetime(df['date_actual'])
    df['longitude'] = pd.to_numeric(df['longitude'])
    df['latitude'] = pd.to_numeric(df['latitude'])

    return df


if __name__ == '__main__':
    print(load_data())
