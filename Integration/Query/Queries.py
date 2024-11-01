class Queries:
    createDatabase = "CREATE DATABASE IF NOT EXISTS Restaurante;"
    useDatabase = "USE Restaurante;"
    dropDatabase = "DROP DATABASE Restaurante;"
    selectCliente = "SELECT * FROM cliente;"
    selectPrato = "SELECT * FROM prato;"
    selectFornecedor = "SELECT * FROM fornecedor;"
    selectIngredientes = "SELECT * FROM ingredientes;"
    selectVenda = "SELECT * FROM venda;"

    def chooseSelect(table):
        return f"SELECT * FROM {table};"