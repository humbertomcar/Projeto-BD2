class Queries:
    
    selectCliente = "SELECT * FROM cliente;"
    selectPrato = "SELECT * FROM prato;"
    selectFornecedor = "SELECT * FROM fornecedor;"
    selectIngredientes = "SELECT * FROM ingredientes;"
    selectVenda = "SELECT * FROM venda;"

    def chooseSelect(table):
        return f"SELECT * FROM {table};"