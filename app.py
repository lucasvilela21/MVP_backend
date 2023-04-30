from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from logger import logger
from schemas import *
from flask_cors import CORS
from model import Session, Artesao, Venda


info = Info(title="MVP API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
artesao_tag = Tag(name="Artesão", description="Adição, visualização e remoção de artesões à base")
venda_tag = Tag(name="Vendas", description="Adição de uma venda de um Artesão cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/artesao', tags=[artesao_tag],
          responses={"200": ArtesaoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_artesao(form: ArtesaoSchema):
    """Adiciona um novo Artesao à base de dados

    Retorna uma representação dos artesões e vendas associados.
    """
    artesao = Artesao(
        box=form.box,
        nome=form.nome,
        celular=form.celular)
    logger.debug(f"Adicionando Artesão no box: '{artesao.box}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando artesão
        session.add(artesao)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado Artesão de nome: '{artesao.nome}'")
        return apresenta_artesao(artesao), 200

    except IntegrityError as e:
        # como a duplicidade do box é a provável razão do IntegrityError
        error_msg = "Box não disponivel para Artesão:/"
        logger.warning(f"Erro ao adicionar Artesão '{artesao.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo artesão :/"
        logger.warning(f"Erro ao adicionar Artesão '{artesao.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/artesoes', tags=[artesao_tag],
         responses={"200": ListagemArtesaoSchema, "404": ErrorSchema})
def get_artesoes():
    """Faz a busca por todos os Artesões cadastrados

    Retorna uma representação da listagem de artesões.
    """
    logger.debug(f"Coletando artesões ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    artesao = session.query(Artesao).all()

    if not artesao:
        # se não há artesões cadastrados
        return {"Artesões": []}, 200
    else:
        logger.debug(f"%d Artesões encontrados" % len(artesao))
        # retorna a representação de artesão
        print(artesao)
        return apresenta_artesoes(artesao), 200


@app.get('/artesao', tags=[artesao_tag],
         responses={"200": ArtesaoViewSchema, "404": ErrorSchema})
def get_artesao(query: ArtesaoBuscaSchema):
    """Faz a busca por um Artesão a partir do box do artesao

    Retorna uma representação dos artesões e vendas associados.
    """
    artesao_box = query.box
    logger.debug(f"Coletando dados sobre Box #{artesao_box}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    artesao = session.query(Artesao).filter(Artesao.box == artesao_box).first()

    if not artesao:
        # se o Artesão não foi encontrado
        error_msg = "Artesão não encontrado na base :/"
        logger.warning(f"Erro ao buscar box '{artesao_box}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Artesao encontrado: '{artesao.nome}'")
        # retorna a representação do artesão
        return apresenta_artesao(artesao), 200


@app.delete('/artesao', tags=[artesao_tag],
            responses={"200": ArtesaoDelSchema, "404": ErrorSchema})
def del_artesao(query: ArtesaoBuscaSchema):
    """Deleta um Artesao a partir do box informado

    Retorna uma mensagem de confirmação da remoção.
    """
    artesao_box = query.box
    logger.debug(f"Deletando dados sobre Box #{artesao_box}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Artesao).filter(Artesao.box == artesao_box).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado box #{print}")
        return {"mesage": "box removido", "box": artesao_box}
    else:
        # se o artesão não foi encontrado
        error_msg = "Box não encontrado na base :/"
        logger.warning(f"Erro ao deletar box #'{artesao_box}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.post('/venda', tags=[venda_tag],
          responses={"200": ArtesaoViewSchema, "404": ErrorSchema})
def add_venda(form: VendaSchema):
    """Adiciona de uma nova venda de um artesao cadastrado na base identificado pelo id

    Retorna uma representação dos artesões e vendas associados.
    """
    artesao_box = form.artesao_box
    logger.debug(f"Adicionando venda ao Artesão de box #{artesao_box}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo Artesão
    artesao = session.query(Artesao).filter(Artesao.box == artesao_box).first()

    if not artesao:
        # se Artesão não encontrado
        error_msg = "Artesão não encontrado na base :/"
        logger.warning(f"Erro ao adicionar venda ao artesão '{artesao_box}', {error_msg}")
        return {"mesage": error_msg}, 404

    # criando o venda
    valor = form.valor
    forma_pagamento = form.forma_pagamento
    venda = Venda(valor,forma_pagamento)

    # adicionando o Venda ao Artesão
    artesao.adiciona_venda(venda)
    session.commit()

    logger.debug(f"Adicionado venda ao artesão de box #{artesao_box}")

    # retorna a representação de Artesão
    return apresenta_artesao(artesao), 200


@app.delete('/venda', tags=[venda_tag],
           responses={"200": VendaDelSchema, "404": ErrorSchema})
def delete_venda(form: VendaBuscaSchema):
    """Remove uma venda de um artesao cadastrado na base identificado pelo ID da venda

    Retorna uma mensagem de confirmação da remoção.
    """
    venda_id = form.id
    logger.debug(f"Deletando dados sobre venda ID #{venda_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Venda).filter(Venda.id == venda_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletada Venda #{print}")
        return {"mesage": "Venda removida", "ID": venda_id}
    else:
        # se o venda não foi encontrada
        error_msg = "Venda não encontrada na base :/"
        logger.warning(f"Erro ao deletar box #'{venda_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    
    
@app.get('/vendas', tags=[venda_tag],
         responses={"200": ListagemVendaSchema, "404": ErrorSchema})
def get_vendas():
    """Faz a busca por todas as vendas cadastradas

    Retorna uma representação da listagem de vendas.
    """
    logger.debug(f"Coletando artesões ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    vendas = session.query(Venda).all()

    if not vendas:
        # se não há artesões cadastrados
        return {"Vendas": []}, 200
    else:
        logger.debug(f"%d Artesões encontrados" % len(vendas))
        # retorna a representação de artesão
        print(vendas)
        return apresenta_vendas(vendas), 200