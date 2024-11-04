import mysql.connector
from Query.Queries import Queries
from Insert.Inserts import Inserts
from CreateDataBase.ConstructDB import ConstructDB

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
        cur.execute(ConstructDB.createDatabase)
        cur.execute(ConstructDB.useDatabase)
        
        def bootstrap(cur):
            
            cur.execute(ConstructDB.createDatabase)
            cur.execute(ConstructDB.useDatabase)

            for table in ConstructDB.constructTables():
                cur.execute(f"{table}")
            for component in ConstructDB.construct():
                cur.execute(f"{component}", multi=True)
            for insert in Inserts.insertDefault():
                cur.execute(f"{insert}")
        
        bootstrap(cur=cur)
        
        db.commit()

        quit = "no"
        while quit == "no":
            options = int(input("[1] CREATE | [2] USE | [3] DROP | [4] SELECT | [5] INSERT\nchoose:"))
            match options:
                case 1:
                    bootstrap(cur)
                case 2: 
                    cur.execute(ConstructDB.useDatabase)

                case 3:
                    cur.execute(ConstructDB.dropDatabase)
                case 4:
                    print("options:\ncliente | prato | fornecedor | ingredientes | venda")
                    table = input("choose the table you want to select: ")

                    cur.execute(Queries.chooseSelect(table=table))
                    for row in cur:
                        print(row)
                case 5:
                    print("options:\ncliente | prato | fornecedor | ingredientes | venda")
                    table = input("choose the table you want to insert: ")
                    
                    match table:
                        case "cliente":
                            args = (input("enter name: "),
                                    input("enter sexo: "),
                                    input("enter idade: "),
                                    input("enter nascimento formato(YYYY-MM-DD): ")
                                )
                            cur.execute(Inserts.newInsertCliente(*args))

                        case "prato":
                            args = (
                                input("enter nome: "),
                                input("enter descricao: "),
                                input("enter valor formato(XXXX.DD): "),
                                input("enter disponibilidade formato(True, False): ")
                            )
                            cur.execute(Inserts.newInsertPrato(*args))

                        case "fornecedor":
                            args = (
                                input("enter nome: "),
                                input("enter estado_origem: ")
                            )
                            cur.execute(Inserts.newInsertFornecedor(*args))
                        case "ingredientes":
                            args = (
                                input("enter nome: "),
                                input("enter data_fabricacão formato(YYYY-MM-DD): "),
                                input("enter data_validade formato(YYYY-MM-DD): "),
                                input("enter quantidade: "),
                                input("enter observacão: ")
                            )
                            cur.execute(Inserts.newInsertIngredientes(*args))

                        case "venda":
                            args = (
                                input("enter id_cliente: "),
                                input("enter id_prato: "),
                                input("enter quantidade: "),
                                input("enter dia formato(YYYY-MM-DD): "),
                                input("enter hora formato(HH:MM:SS): "),
                                input("enter valor formato(XXXX.DD): ")
                            )
                            cur.execute(Inserts.newInsertVenda(*args))
                    
                    db.commit()
            quit = input("do you want to quit?\nyes | no\n")
                    
        cur.close()
        db.close()