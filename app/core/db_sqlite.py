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
    """Busca informações de produtos, suas características e preços no banco via SQLite. Considere o seguinte schema e uma pequena amostra da tabela 'produtos':
    [(0, 'index', 'BIGINT', 0, None, 0), (1, 'productId', 'BIGINT', 0, None, 0), (2, 'title', 'TEXT', 0, None, 0), (3, 'price', 'FLOAT', 0, None, 0), (4, 'image', 'TEXT', 0, None, 0), (5, 'description', 'TEXT', 0, None, 0)]

    [(1666, 2009094, 'camisa manga longa com bolso branco', 139.99, 'https://cea.vteximg.com.br/arquivos/ids/57197111/camisa-manga-longa-com-bolso-branco-7591834-Branco_1.jpg?v=638128914633000000', 'camisa manga longa bolso branco moda masculina roupas blusas 1 2 3 4 5 6 7'), (1667, 2017098, 'camisa manga curta com bolso branca', 119.99, 'https://cea.vteximg.com.br/arquivos/ids/53195213/camisa-manga-curta-com-bolso-branco-7602490-Branco_1.jpg?v=637801158434200000', 'camisa manga curta bolso branca moda masculina roupas blusas branco 3 4 5 2 1 6 7'), (1326, 2062137, 'Calça Jeans Feminina Super Skinny com Zíper na Barra Azul Médio', 119.99, 'https://cea.vteximg.com.br/arquivos/ids/52448505/Calca-Jeans-Feminina-Super-Skinny-com-Ziper-na-Barra-Azul-Medio-7936103-Azul_Medio_1.jpg?v=637774164382300000', 'calca jeans feminina super skinny ziper barra azul medio moda roupas calcas 40 46 36 38 44 42 48 34')]
    """    
    try:
        df = pd.read_sql_query(query, conn)
        if df.empty:
            return "Nenhum resultado encontrado."
        return df.to_string(index=False)
    except Exception as e:
        return f"Erro na consulta SQL: {str(e)}"