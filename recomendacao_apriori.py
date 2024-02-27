import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
from itertools import permutations


def load_data(file_path):
    """
    Carrega os dados do arquivo CSV e retorna um DataFrame pandas.
    """
    return pd.read_csv(file_path)


def pivot_data(df):
    """
    Pivota os dados do DataFrame para criar uma tabela de transações.
    """
    df_pivot = df.pivot_table(index='external_order_reference',
                              columns=df.groupby('external_order_reference').cumcount(), values='descriptionsku',
                              aggfunc='first')
    df_pivot.columns = [f'item_{col}' for col in df_pivot.columns]
    df_pivot.fillna(0, inplace=True)
    return df_pivot.reset_index(drop=True)


def preprocess_data(pivot_df):
    """
    Remove zeros e converte o DataFrame pivotado em uma lista de listas.
    """
    return pivot_df.apply(lambda row: list(filter(lambda x: x != 0, row)), axis=1).tolist()


def generate_association_rules(transactions, min_support=0.02, min_confidence=0.6):
    """
    Gera as regras de associação a partir das transações usando Apriori.
    """
    te = TransactionEncoder()
    te_array = te.fit(transactions).transform(transactions)
    pedidos_encoding = pd.DataFrame(te_array, columns=te.columns_)

    frequent_items = apriori(pedidos_encoding, min_support=min_support, use_colnames=True)
    rules = association_rules(frequent_items, metric="confidence", min_threshold=min_confidence)
    return rules


def get_top_products_by_buyer(pedidos_df, buyer, n=5):
    """
    Retorna os N produtos mais comprados pelo comprador especificado.
    """
    pedidos_buyer_df = pedidos_df[pedidos_df['external_buyer_reference'] == buyer]
    top_products_buyer = pedidos_buyer_df['descriptionsku'].value_counts().head(n).reset_index()
    top_products_buyer.columns = ['product', 'frequency']
    return top_products_buyer


def generate_combinations(products):
    """
    Gera todas as combinações possíveis de produtos.
    """
    combinations = []
    lista_frozensets = []
    for r in range(1, len(products) + 1):
        combinations.extend(list(permutations(products, r)))
    comb_produtos = [list(item) for item in combinations]
    for prod in comb_produtos:
        produto_fset = frozenset(prod)
        lista_frozensets.append(produto_fset)
    return lista_frozensets

def filter_rules_by_products(rules, products):
    """
    Filtra as regras de associação para incluir apenas aquelas relacionadas aos produtos fornecidos.
    """
    selected_rules = rules[rules['antecedents'].isin(products)]
    recommended_products = selected_rules['consequents'].explode().unique()
    return pd.DataFrame({'product': recommended_products})


def main(buyer):
    # Carregar dados
    file_path = r'C:\Users\artur\PycharmProjects\pythonProject\AlgoritmoRecomendacao\tmp_pedidos_tiscoski.csv'
    pedidos_df = load_data(file_path)

    # Pivotar dados
    pivot_df = pivot_data(pedidos_df)

    # Pré-processamento
    transactions = preprocess_data(pivot_df)

    # Gerar regras de associação
    rules = generate_association_rules(transactions)

    # Obter os produtos mais comprados pelo comprador
    top_products_buyer = get_top_products_by_buyer(pedidos_df, buyer)

    # Gerar combinações de produtos
    product_combinations = generate_combinations(top_products_buyer['product'].tolist())

    # Filtrar regras de associação para produtos específicos
    recommended_products = filter_rules_by_products(rules, product_combinations)

    # Resultado final
    recommended_products['buyer'] = buyer
    output = recommended_products[['buyer', 'product']].to_json(orient='records')

    return output

if __name__ == "__main__":
    buyer = "0015f00000jkOhoAAE"
    #buyer = input('Digite: ')
    a = main(buyer)
    print(a)


