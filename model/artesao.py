from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from  model import Base , Venda

class Artesao(Base):
    __tablename__ = 'artesao_table'
 
    box = Column("pk_artesao", Integer, primary_key=True)
    nome =  Column(String(140), unique=True)
    celular = Column(String(14))
    # Definição do relacionamento entre o Artesao e a venda.
    vendas = relationship("Venda")

    def __init__(self, box:Integer, nome:String, celular:String = None):
        """
        Cria um artesão

        Arguments:
            box: Numero do Box do Artesão 
            nome: Nome do Artesão.
            celular: Celular do Artesão 
        """
        self.box = box
        self.nome = nome
        self.celular = celular

    def adiciona_venda(self, venda:Venda):
        """ Adiciona uma nova venda pro Artesão
        """
        self.vendas.append(venda)