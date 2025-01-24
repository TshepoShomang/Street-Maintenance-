import pyodbc

conn = pyodbc.connect('DRIVER={SQL SERVER};'
                       'SERVER=DESKTOP-S1F7VIB;'
                       'DATABASE=SyruProjects;'
                      )

cursor = conn.cursor()





def insert(email, username, password, role = 'Client'):
    sql_insert = "INSERT INTO Person (email, username, password, role) VALUES (?,?,?,?)"
    data = (email,username,password, role)
    
    try:
        cursor.execute(sql_insert, data)
        conn.commit()
        print("Data inserted successfully")
        
    except Exception as e:
        conn.rollback()
        print("Error inserting data: ", e)
        
    cursor.close()
    conn.close()
    
def setService(email, service):
    sql_insert = "INSERT INTO Service (email, service) VALUES (?,?)"
    data = (email,service)
    
    try:
        cursor.execute(sql_insert, data)
        conn.commit()
        print("Data inserted successfully")
        
    except Exception as e:
        conn.rollback()
        print("Error inserting data: ", e)
        
    cursor.close()
    conn.close()