from pydantic import BaseModel
from typing import Optional, List
from model.artesao import Artesao

from schemas import VendaSchema


class ArtesaoSchema(BaseModel):
    """ Define como um novo Artesao a ser inserido deve ser representado
    """
    box: int = 1
    nome: str = "Lucas Vilela"
    celular: str = "(DD)XXXXX-XXXX"


class ArtesaoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do Artesão.
    """
    box: int = 1


class ListagemArtesaoSchema(BaseModel):
    """ Define como uma listagem de Artesões será retornada.
    """
    artesoes:List[ArtesaoSchema]


def apresenta_artesoes(artesoes: List[Artesao]):
    """ Retorna uma representação do Artesao seguindo o schema definido em
        ArtesaoViewSchema.
    """
    result = []
    for artesao in artesoes:
        result.append({
            "box": artesao.box,
            "nome": artesao.nome,
            "celular": artesao.celular,
        })

    return {"Artesões": result}


class ArtesaoViewSchema(BaseModel):
    """ Define como um Artesão será retornado: Artesão + Vendas.
    """
    box: int = 1
    nome: str = "Lucas Vilela"
    celular: Optional[str] = "(DD)XXXXX-XXXX"
    total_vendas: int = 1
    vendas:List[VendaSchema]


class ArtesaoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_artesao(artesao: Artesao):
    """ Retorna uma representação do artesão seguindo o schema definido em
        ArtesaoViewSchema.
    """
    return {
        "box": artesao.box,
        "nome": artesao.nome,
        "celular": artesao.celular,
        "total_vendas": len(artesao.vendas),
        "vendas": [{"Valor": venda.valor} for venda in artesao.vendas]
    }


   
