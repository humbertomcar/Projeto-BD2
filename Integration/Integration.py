import mysql.connector
from Query.Queries import Queries as q
from Insert.DefaultInsert import DefaultInsert

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

        defaultCur = db.cursor()
        defaultCur.execute(q.useDatabase)
        defaultCur.execute(DefaultInsert.insertDefault(), multi=True)
        defaultCur.close()
        cur = db.cursor()
        db.commit()

        quit = "no"
        while quit == "no":
            options = input("[1] CREATE | [2] USE | [3] DROP | [4] INSERT\nchoose:")
            match options:
                case 1:
                    cur.execute(q.createDatabase)
                case 2: 
                    cur.execute(q.useDatabase)
                case 3:
                    cur.execute(q.dropDatabase)


            quit = input("do you want to quit?\nyes | no\n")
        
        cur.close()
        db.close()