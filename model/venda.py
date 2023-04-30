from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from datetime import datetime
from typing import Union

from  model import Base

class Venda(Base):
    __tablename__ = 'venda_table'

    id = Column(Integer, primary_key=True)
    valor = Column(Float)
    forma_pagamento = Column(String(8), default = 'Dinheiro')
    data_insercao = Column(DateTime, default=datetime.now())
    # Definição do relacionamento entre o Vendas e o Artesão.
    box_artesao = Column(Integer, ForeignKey("artesao_table.pk_artesao"), nullable=False)

    def __init__(self, valor:float, forma_pagamento:String, data_insercao:Union[DateTime, None] = None):
        """
        Cria uma Venda

        Arguments:
            nome: Valor da venda.
            forma_pagamento: Forma de Pagamento (Debito, Credito ou Dinheiro)
            data_insercao: data de quando a venda foi inserida à base
        """
        self.valor = valor
        self.forma_pagamento = forma_pagamento
        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

