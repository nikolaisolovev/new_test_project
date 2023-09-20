import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
import os


df = pd.read_excel('data.xlsx')

"""
Общая выручка за июль 2021 по тем сделкам, приход денежных средств которых не просрочен
"""
new_df = df.loc[259:368,["sum", "status"]]
total_july_amount = new_df[new_df.status != 'ПРОСРОЧЕНО'].sum()['sum']
print('Общая выручка за июль 2021 по тем сделкам, приход денежных средств которых не просрочен\n',
       total_july_amount)


"""
Выручка компании за рассматриваемый период. График.
"""
new_df[new_df.status != 'ПРОСРОЧЕНО']['sum'].plot()
plt.show()


"""
Кто из менеджеров привлек для компании больше всего денежных средств в сентябре 2021
"""
sept_df = df.loc[485:593, ['sum', 'sale']]

result_df = sept_df.groupby('sale')['sum'].sum().reset_index()
result_df = result_df.sort_values(by='sum', ascending=False)
result_df = result_df.head(1)

print('Больше всего денежных средств в сентябре 2021:\n', result_df)


"""
Тип сделок (новая/текущая), преобладающий в октябре 2021
"""
oct_df = df.loc[595:729, ['new/current']]
result = oct_df.groupby('new/current').size().reset_index(name='quantity')
result = result.sort_values(by='quantity', ascending=False).head(1)

print(result)


"""
Количество оригиналов договора по майским сделкам в июне 2021
"""

may_df = df.loc[1:128, ['document', 'receiving_date']]

may_df['receiving_date'] = may_df['receiving_date'].astype(str)
filtered_df = may_df[(may_df['receiving_date'].str.contains('2021-06-')) & (may_df['document'] == 'оригинал')]

result = filtered_df.groupby('document').size().reset_index(name='quantity_of_original')

print('Количество оригиналов договора по майским сделкам в июне 2021: \n', result)
