########################################################
#           WELCOME TO AMELIA DATA ACCESS!             #
#                ver. 2.1.0.0 - Brigadeiro             #
#                                                      #
#             -WHAT DOES THIS LIB DO?-                 #
#    MAKE YOUR LIFE EASIER WITH SIMPLE CONNECTION      #
#                   WITH MARIADB                       #
#                                                      #
#             -WHY THE NAME 'AMELIA'?-                 #
#   SEE https://bit.ly/2WgIsm2 - NO VIRUS, TRUST ME    #
#                                                      #
#                -WHY CHOOSE AMELIA?-                  #
#     BECAUSE IT'S SIMPLE, FREE AND OPEN... DUH?       #   
#                                                      #
#                -HOW DO I USE IT?-                    #
#           FIRST, IMPORT IT TO YOUR .py               #
#                 SECOND, TWO WAYS:                    #
#  _AMELIAGO                                           #
#  USING THIS "MOTHER METHOD", YOU JUST USE THE LIST   #
#       WITH CONNECTION AND WHAT YOU WANNA DO.         #
#                                                      #
#  _GO THROUGH ALL                                     #
# WE RECOMMEND THIS FOR SOMETHING EDUCATION, DIDACTIC  #
#  WORK THE SAME AS THE AMELIAGO BUT WITH STEPS MADE   #
#              BY YOU, LIKE THIS ONE:                  #      
#                                                      #
#conn = baseConnect('0.0.0.0', 'root', 'root', 'test') #
#lcursor = conn.cursor()                               #
#query = simpleSqlOpen(lcursor, "select * from test")  #
#content = (query)                                     #
#                                                      #
#               ---- CHANGE LOG ----                   #
#                                                      #
# - 2.1.0.0 - Brigadeiro -                             #
#   - BUGFIX - I forgot to update simpleSqlOpen        #
#                                                      #
# - 2.0.0.0 - Brigadeiro -                             #
#   - BUGFIX - Add column names at the resultset       #
#   - NEW FUNCION - Multi RecordSet embedded now       #
#                                                      #
# - 1.0.1.0 - Cocada - Amelia's birth                  #
#                                                      #
#              Created by RealMr_Glasses               #
########################################################



import mysql.connector as mariadb

#status functions -------------------------------------------------------------------------------------------------------------
def isAlive(Aconfig):
    "Alive? Maybe. - Configuration like preloadConnect - list with HOST, USER, PASS and DB"
    try:
        mariadb_connection = mariadb.connect(host=Aconfig[0], user=Aconfig[1], password=Aconfig[2], database=Aconfig[3])
        mariadb_connection.close()
        return 'Yup.'
    except BaseException as e:
        return 'Nope. Error: ' + str(e) 

def isAliveFV(Ahost, Auser, Apass, Adb):    
    "Alive? Maybe. (Full version)"
    try:
        mariadb_connection = mariadb.connect(host=Ahost, user=Auser, password=Apass, database=Adb)
        mariadb_connection.close()
        return 'Yup.'
    except BaseException as e:
        return 'Nope. Error: ' + str(e) 

#Connection functions ---------------------------------------------------------------------------------------------------------
def baseConnect(Ahost, Auser, Apass, Adb):
    """Create a cursor for the conection with database. Don't forget to make a return.close() """
    try:
       mariadb_connection = mariadb.connect(host=Ahost, user=Auser, password=Apass, database=Adb) 
       #cursor = mariadb_connection.cursor()
       return mariadb_connection
    except BaseException as e:
        return 'Error: ' + str(e)
        #return None

def preloadConnect(Aconfig):
    """Create a cursor for the conection with database with a preload configuration. Configuration: list with HOST, USER, PASS and DB.Don't forget to make a return.close()"""
    try:
       mariadb_connection = mariadb.connect(host=Aconfig[0], user=Aconfig[1], password=Aconfig[2], database=Aconfig[3]) 
       #cursor = mariadb_connection.cursor()
       return mariadb_connection
    except BaseException as e:
        return 'Error: ' + str(e)
        #return None

#True SQL functions
def simpleSqlOpen(Acursor, Atext):
    """Returns a SQL query with all lines."""
    try:
        Acursor.execute(Atext)
        result = Acursor.fetchall()
        
        listR = []
        for result in Acursor.stored_results():
            row_headers = [x for x in result.column_names]  #column names
            resultSet = result.fetchall()
            dataSet = []
            for line in resultSet:
                dataSet.append(dict(zip(row_headers,line)))
            listR.append(dataSet)

        return listR #Multi RecordSet embedded

        #return result
    except BaseException as e:
        return 'Error: ' + str(e)
    
def simpleSqlExec(Acursor, Atext):
    """Execute a SQL query. Don't forget the connection.commit() or connection.rollback() after this command."""
    try:
        Acursor.execute(Atext)
        Acursor.fetchall()
        # result.commit()
        return True
    except BaseException as e:
        return 'Error: ' + str(e)

def simpleSqlProcOpen(Acursor, Aproc, Aparams):
    """Execute a procedure in and returns a SQL query with all lines."""
    try:
        Acursor.callproc(Aproc, Aparams)
        listR = []
        for result in Acursor.stored_results():
            row_headers = [x for x in result.column_names]  #column names
            resultSet = result.fetchall()
            dataSet = []
            for line in resultSet:
                dataSet.append(dict(zip(row_headers,line)))
            listR.append(dataSet)

        return listR #Multi RecordSet embedded
    except BaseException as e:
        return 'Error: ' + str(e)

def simpleSqlProcExec(Acursor, Aproc, Aparams):
    """Execute a SQL stored procedures. Don't forget the connection.commit() or connection.rollback() after this command."""
    try:
        Acursor.callproc(Aproc, Aparams)
        Acursor.fetchall()
        # result.commit()
        return True
    except BaseException as e:
        return 'Error: ' + str(e)


#AMELIAGO - Complete connections to sql------------------------------------------------------------------------------------------------
def ameliaGoOpenSql(Aconfig, Atext):
    """Connect and return a simple select from MariaDB. Always check for errors, please."""
    conn = preloadConnect(Aconfig)
    if isinstance(conn, str):
        return conn
    else:
        cur = conn.cursor()
        generalResult = simpleSqlOpen(cur, Atext)
        cur.close()
        conn.close()
        return generalResult

def ameliaGoExecSql(Aconfig, Atext):
    """Connect and return true or error message from a simple exec from MariaDB. Always check for errors, please."""
    conn = preloadConnect(Aconfig)
    if isinstance(conn, str):
        return conn
    else:
        cur = conn.cursor()
        generalResult = simpleSqlExec(cur, Atext)
        if generalResult:
            conn.commit()
        else:
            conn.rollback()
        cur.close()
        conn.close()
        return generalResult

def ameliaGoProcOpen(Aconfig, Aproc, Aparams):
    """Connect and return the resultSet or error from a stored procedure from MariaDB. Always check for errors, please."""
    conn = preloadConnect(Aconfig)
    if isinstance(conn, str):
        return conn
    else:
        cur = conn.cursor()
        generalResult = simpleSqlProcOpen(cur, Aproc, Aparams)
        cur.close()
        conn.close()
        return generalResult

def ameliaGoProcExec(Aconfig, Aproc, Aparams):
    """Connect and execute the stored procedure from MariaDB. Always check for errors, please."""
    conn = preloadConnect(Aconfig)
    if isinstance(conn, str):
        return conn
    else:
        cur = conn.cursor()
        generalResult = simpleSqlProcExec(cur, Aproc, Aparams)
        if generalResult:
            conn.commit()
        else:
            conn.rollback()
        cur.close()
        conn.close()
        return generalResult