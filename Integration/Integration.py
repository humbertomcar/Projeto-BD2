import mysql.connector
from Query.Queries import Queries as q

class Integration:

    user = input("enter your database user: ")
    passwd = input("enter your databse password: ")

    try:
        db = mysql.connector.connect(
            host="localhost",
            user=f"{user}",
            passwd=f"{passwd}"
        )
    except Exception:
        print("couldn`t connect to database, please check your user and password :)")
    
    else:
        
        quit = "no"
        cur = db.cursor()
        cur.execute

        while quit == "no":
            options = input("[1] CREATE | [2] USE | [3] DROP | [4] SELECT\nchoose:")
            match options:
                case 1:
                    cur.execute(q.createDatabase)
                case 2: 
                    cur.execute(q.useDatabase)
                case 3:
                    cur.execute(q.dropDatabase)

            quit = input("do you want to quit?\nyes | no\n")