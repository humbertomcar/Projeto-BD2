class Cliente:
    
    def __init__(self, nome, descricao, valor, disponibilidade):
        self.nome = nome
        self.descricao = descricao
        self.valor = valor
        self.disponibilidade = disponibilidade

    def newInsert(self):
        result = f"""
            INSERT INTO cliente (nome, descricao, valor, disponibilidade) VALUES
            ('{self.nome}', '{self.descricao}', {self.valor}, {self.disponibilidade})
        """
        return result