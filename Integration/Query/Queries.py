class Queries:

    def chooseSelect(table):
        return f"SELECT * FROM {table};"
    
    callSorteio = "CALL Sorteio();"
    callEstatisticas = "CALL Estatisticas_Venda()"
    
    def callReajuste(numDecimal):
        return f"CALL Reajuste({numDecimal})"
    
    def callGastarPontos(idCliente, idPrato):
        return f"CALL Reajuste({idCliente}, {idPrato})"
        