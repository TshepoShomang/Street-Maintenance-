import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import pypyodbc as odbc
import json


SERVER_NAME = 'DESKTOP-S1F7VIB'
DATABASE_NAME = 'SyruProjects'

connection_string = f"""
    Driver={{SQL Server}};
    Server={SERVER_NAME};
    Database={DATABASE_NAME};
    Trusted_Connection=yes;
"""
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
engine = create_engine(connection_url, module=odbc)




#this function takes emails from the database and puts them in a pandas dataframe
def prevUser():
    sql_statement = """
        SELECT * FROM Person
    """
    df = pd.read_sql_query(sql_statement, engine)
    df = df.email.tolist()
    return df

def userNames():
    sql_statement = """
        SELECT * FROM Person
    """
    df = pd.read_sql_query(sql_statement, engine)
    df = df.username.tolist()
    return df


def getUsername(email):
    sql_statement = f"""
        SELECT * FROM Person WHERE email = '{email}'
    """
    df = pd.read_sql_query(sql_statement, engine)
    df = df.username.tolist()
    return df


def getPassword(email):
    sql_statement = f"""
        SELECT * FROM Person WHERE email='{email}'
    """
    df = pd.read_sql_query(sql_statement, engine)
    df = df.password.tolist()
    return df[0]

def getRole(email):
    sql_statement = f"SELECT * FROM Person WHERE email='{email}'"
    df = pd.read_sql_query(sql_statement, engine)
    df = df.role.tolist()
    return df[0]

