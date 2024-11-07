import mysql.connector
from Query.Queries import Queries
from Insert.Inserts import Inserts
from CreateDataBase.ConstructDB import ConstructDB
from CreateDataBase.ConstructProcedures import ConstructProcedures

class Integration:

    print("users:\nadministrador | gerente | funcionario")
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
            
            for user in ConstructDB.createUsers():
                cur.execute(f"{user}", multi=True)
            
            for table in ConstructDB.createTables():
                cur.execute(f"{table}")
            
            for dropProcedure in ConstructProcedures.dropProcedures():
                cur.execute(f"{dropProcedure}")

            for procedure in ConstructProcedures.createProcedures():
                cur.execute(f"{procedure}")

            for view in ConstructDB.createViews():
                cur.execute(f"{view}")

            for trigger in ConstructDB.createTriggers():
                cur.execute(f"{trigger}")
            
            for insert in Inserts.insertDefault():
                cur.execute(f"{insert}")
            
        db.commit()

        quit = "no"
        while quit == "no":
            options = int(input("[1] CREATE | [2] USE | [3] DROP | [4] SELECT | [5] INSERT | [6] PROCEDURES\nchoose: "))
            match options:
                case 1:
                    bootstrap(cur)
                case 2: 
                    cur.execute(ConstructDB.useDatabase)

                case 3:
                    cur.execute(ConstructDB.dropDatabase)
                case 4:
                    print("""options:\ncliente | prato | fornecedor | ingredientes | venda | usos
VendasPorCliente | ClientesEVendas | TotalGastoPorCliente | ClienteComMaisVendas""")
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
                                input("enter valor formato(DECIMAL): "),
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
                                input("enter valor formato(DECIMAL): ")
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
                    print("options:\n[1] Sorteio() | [2] Estatisticas_Venda() | [3] Gastar_pontos(id_cliente, id_prato) | [4] Reajuste(DECIMAL)")
                    procedure = int(input("choose the procedure you want to use: "))

                    match procedure:
                        case 1:
                            cur.callproc(Queries.callSorteio)

                        case 2:
                            cur.callproc(Queries.callEstatisticas)
                            cur.execute("SELECT * FROM resultado_estatisticas")
                            for row in cur:
                                print(row)
                            cur.execute("DROP TEMPORARY TABLE resultado_estatisticas;")
                        
                        case 3:
                            args = (input("enter id cliente: "),
                                    input("enter id prato: ")
                                )
                            cur.callproc("Gastar_Pontos", [*args])
                        
                        case 4:
                            numDecimal = input("enter decimal number (INT): ")

                            cur.callproc('Reajuste', [numDecimal])
                    db.commit()

            quit = input("do you want to quit?\nyes | no\n")
                    
        cur.close()
        db.close()