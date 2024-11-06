import mysql.connector
from Query.Queries import Queries
from Insert.Inserts import Inserts
from CreateDataBase.ConstructDB import ConstructDB
from CreateDataBase.ConstructProcedures import ConstructProcedures

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
        
        def bootstrap(cur):
            
            cur.execute(ConstructDB.createDatabase)
            cur.execute(ConstructDB.useDatabase)
            
            for table in ConstructDB.constructTables():
                cur.execute(f"{table}")
            
            cur.execute(ConstructProcedures.dropProcedureSorteio)
            cur.execute(ConstructProcedures.createProcedureSorteio)

            # for component in ConstructDB.construct():
            #     cur.execute(f"{component}", multi=True)
            for insert in Inserts.insertDefault():
                cur.execute(f"{insert}")
            

        bootstrap(cur=cur)
        
        db.commit()

        quit = "no"
        while quit == "no":
            options = int(input("[1] CREATE | [2] USE | [3] DROP | [4] SELECT | [5] INSERT | [6] PROCEDURES\nchoose:"))
            match options:
                case 1:
                    bootstrap(cur)
                case 2: 
                    cur.execute(ConstructDB.useDatabase)

                case 3:
                    cur.execute(ConstructDB.dropDatabase)
                case 4:
                    print("options:\ncliente | prato | fornecedor | ingredientes | venda | usos")
                    table = input("choose the table you want to select: ")

                    cur.execute(Queries.chooseSelect(table=table))
                    for row in cur:
                        print(row)
                case 5:
                    print("options:\ncliente | prato | fornecedor | ingredientes | venda | usos")
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
                        case "usos":
                            args = (
                                input("enter id prato: "),
                                input("enter id ingrediente: ")
                            )
                            cur.execute(Inserts.newInsertUsos(*args))
                    db.commit()
                case 6:
                    print("options:\n[1] Sorteio | [2] Estatisticas_Venda() | [3] Gastar_pontos(id_cliente, id_prato) | [4] Reajuste(XXXX.DD)")
                    procedure = input("choose the procedure you want to use: ")

                    match procedure:
                        case 1:
                            cur.callproc(Queries.callSorteio)
                        case 2:
                            cur.callproc(Queries.callEstatisticas)
                            for row in cur:
                                print(row)
                        case 3:

                            idClient = input("enter id cliente: ")
                            idPrato = input("enter id prato: ")

                            cur.callproc(Queries.callGastarPontos(idCliente=idClient, idPrato=idPrato))
                        case 4:
                            numDecimal = input("enter decimal number (XXXXX.DD)")

                            cur.callproc(Queries.callReajuste(numDecimal=numDecimal))
                    db.commit()

            quit = input("do you want to quit?\nyes | no\n")
                    
        cur.close()
        db.close()