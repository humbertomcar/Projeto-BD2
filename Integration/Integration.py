import mysql.connector
from Query.Queries import Queries
from Insert.DefaultInsert import DefaultInsert as di

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

        cur = db.cursor()
        cur.execute(Queries.useDatabase)
        for insert in di.insertDefault():
            cur.execute(insert)
        
        db.commit()

        quit = "no"
        while quit == "no":
            options = int(input("[1] CREATE | [2] USE | [3] DROP | [4] SELECT\nchoose:"))
            match options:
                case 1:
                    cur.execute(Queries.createDatabase)
                case 2: 
                    cur.execute(Queries.useDatabase)
                case 3:
                    cur.execute(Queries.dropDatabase)
                case 4:
                    print("options:\ncliente | prato | fornecedor | ingredientes | venda")
                    table = input("choose the table you want to select: ")

                    cur.execute(Queries.chooseSelect(table=table))
                    for row in cur:
                        print(row)

            quit = input("do you want to quit?\nyes | no\n")
        
        cur.close()
        db.close()