class Venda:
    
    def __init__(self, id_cliente, id_prato, quantidade, dia, hora, valor):
        self.id_cliente = id_cliente
        self.id_prato = id_prato
        self.quantidade = quantidade
        self.dia = dia
        self.hora = hora
        self.valor = valor

    def newInsert(self):
        result = f"""
            INSERT INTO cliente (id_cliente, id_prato, quantidade, dia, hora, valor) VALUES
            ({self.id_cliente}, {self.id_prato}, {self.quantidade}, '{self.dia}', '{self.hora}', {self.valor})
        """
        return result