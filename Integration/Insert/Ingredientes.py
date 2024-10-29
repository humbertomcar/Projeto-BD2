class Ingredientes:
    
    def __init__(self, nome, data_fabricacao, data_validade, quantidade, observacao):
        self.nome = nome
        self.data_fabricacao = data_fabricacao
        self.data_validade = data_validade
        self.quantidade = quantidade
        self.observacao = observacao

    def newInsert(self):
        result = f"""
            INSERT INTO ingredientes (nome, data_fabricacao, data_validade, quantidade, observacao) VALUES
            ('{self.nome}', '{self.data_fabricacao}', '{self.data_validade}', {self.quantidade}, '{self.observacao}')
        """
        return result