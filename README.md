# Minha API MVP

Projeto de MVP para conclusão do Sprint I da Pós Graduação em Engenharia de Software pela PUC-RIO.

Projeto com finalidade de cadastrar Artesões e Vendas dos Artesões, para futuro uso em uma feira de voluntários da APAE de 
Mogi das Cruzes.

Requisitos adicionais da API levantados pelo autor do Projeto:
1) Banco de dados deve ter duas tabelas: Artesões e Vendas;
2) Tabela de Artesão deve aceitar apenas um artesão por Box;
3) Tabela vendas deve registrar o horario da venda;
4) Tabela vendas deve registar se a compra foi em Dinheiro, Crédito ou Débito;

---
## Como executar 

Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5001
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5001 --reload
```

Abra o [http://localhost:5001/#/](http://localhost:5001/#/) no navegador para verificar o status da API em execução.
