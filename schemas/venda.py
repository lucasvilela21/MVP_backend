from pydantic import BaseModel
from typing import List
from model.venda import Venda

class VendaSchema(BaseModel):
    """ Define como um nova venda a ser inserido deve ser representado
    """
    artesao_box: int = 1
    valor: float = 10.00
    forma_pagamento: str = "Dinheiro"

class VendaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do Artesão.
    """
    id: int = 1

class VendaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str


class ListagemVendaSchema(BaseModel):
    """ Define como uma listagem de Artesões será retornada.
    """
    venda:List[VendaSchema]


def apresenta_vendas(vendas: List[Venda]):
    """ Retorna uma representação de Venda seguindo o schema definido em
        VendaViewSchema.
    """
    result = []
    for venda in vendas:
        result.append({
            "box": venda.box_artesao,
            "valor": venda.valor,
            "forma de pagamento": venda.forma_pagamento,
        })

    return {"Vendas": result}
