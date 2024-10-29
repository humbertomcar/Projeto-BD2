class Fornecedor:
    
    def __init__(self, nome, estado_origem):
        self.nome = nome
        self.estado_origem = estado_origem

    def newInsert(self):
        result = f"""
            INSERT INTO fornecedor (nome, estado_origem) VALUES
            ('{self.nome}', '{self.estado_origem}')
        """
        return result