
import pandas as pd

buyer = "0015f00000jkQzgAAE"
pedidos_df = pd.read_csv(r'C:\Users\artur\PycharmProjects\pythonProject\AlgoritmoRecomendacao\tmp_pedidos_tiscoski.csv')
pedidos_buyer_df = pedidos_df[pedidos_df['external_buyer_reference'] == buyer]
top_products_buyer = pedidos_buyer_df['descriptionsku'].value_counts().head(5).reset_index()
top_products_buyer.columns = ['product', 'frequency']

print(top_products_buyer)
