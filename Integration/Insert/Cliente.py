class Cliente:
    
    def __init__(self, nome, sexo, idade, nascimento):
        self.nome = nome
        self.sexo = sexo
        self.idade = idade
        self.nascimento = nascimento

    def newInsert(self):
        result = f"""
            INSERT INTO cliente (nome, sexo, idade, nascimento) VALUES
            ('{self.nome}', '{self.sexo}', {self.idade}, '{self.nascimento}')
        """
        return result