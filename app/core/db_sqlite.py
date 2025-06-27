import sqlite3
import pandas as pd

DB_PATH = "app/db/produtos.db"
JSON_PATH = "data/dados-produtos.json"

conn = sqlite3.connect(DB_PATH, check_same_thread=False)

def init_produtos_table():
    """Inicializa a tabela de produtos no banco de dados SQLite a partir de um arquivo JSON."""
    df = pd.read_json(JSON_PATH)
    df.to_sql("produtos", conn, if_exists="replace", index=False)

init_produtos_table()

def search_sql(query: str) -> str:
    """Busca informações de produtos, suas características e preços no banco via SQL. Considere o seguinte schema da tabela produtos:\n\n
    |      |   productId | title                                                                  |   price | image                                                                                                                                                      | description                                                                                                                      |
|-----:|------------:|:-----------------------------------------------------------------------|--------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------|
|  835 |     4494421 | calça wide leg de sarja cintura alta com nervura sawary bege           |  199.99 | https://cea.vteximg.com.br/arquivos/ids/58909977/Foto-0.jpg?v=638590696067070000                                                                           | calca wide leg sarja cintura alta nervura sawary bege moda feminina roupas calcas areia 38 34 36 40 44 42 46                     |
| 2209 |     2493999 | Camisa Infantil Estampada Xadrez Manga Longa Azul Marinho              |   89.99 | https://cea.vteximg.com.br/arquivos/ids/54461993/Camisa-Infantil-Estampada-Xadrez-Manga-Longa-Azul-Marinho-9808445-Azul_Marinho_1.jpg?v=637889181464900000 | camisa infantil estampada xadrez manga longa azul marinho roupas blusas 4 6 8 10 12                                              |
|  945 |     4502674 | calça jogger de sarja infantil verde                                   |  109.99 | https://cea.vteximg.com.br/arquivos/ids/59012332/Foto-0.jpg?v=638621774375970000                                                                           | calca jogger sarja infantil verde roupas calcas 1 2 3 4 5                                                                        |
|  579 |     4467534 | calça de sarja wide leg cropped cintura super alta bege                |  159.99 | https://cea.vteximg.com.br/arquivos/ids/58640920/Foto-0.jpg?v=638512924258300000                                                                           | calca sarja wide leg cropped cintura super alta bege moda feminina roupas calcas kaki 44 34 38 48 40 46 36 42                    |
|  444 |     4455809 | calça jeans reta copenhagen animal print cintura alta mindset colorida |  239.99 | https://cea.vteximg.com.br/arquivos/ids/59061919/Foto-0.jpg?v=638648727190900000                                                                           | calca jeans reta copenhagen animal print cintura alta mindset colorida moda feminina roupas calcas multicor 34 38 40 44 42 46 36 |
"""    
    try:
        df = pd.read_sql_query(query, conn)
        if df.empty:
            return "Nenhum resultado encontrado."
        return df.to_string(index=False)
    except Exception as e:
        return f"Erro na consulta SQL: {str(e)}"