import pyodbc

conn = pyodbc.connect('DRIVER={SQL SERVER};'
                       'SERVER=DESKTOP-S1F7VIB;'
                       'DATABASE=SyruProjects;'
                      )

cursor = conn.cursor()

def updateRole(role, username):

    update_query = "UPDATE Person SET role = CAST(? AS VARCHAR(MAX)) WHERE username = CAST(? AS VARCHAR(MAX))"


    cursor.execute(update_query, (role, username))


    conn.commit()
    print (f'role for {username} has been updated to {role}')


    cursor.close()
    conn.close()


