"""
Бонусы по сделкам
"""


import pandas as pd
import numpy as np


df = pd.read_excel('data.xlsx')

may_df = df.loc[2:128]

may_df['receiving_date'] = may_df['receiving_date'].astype(str)

conditions = [
    ((may_df['new/current'] == 'новая') & (may_df['status'] == 'ОПЛАЧЕНО') &
     (may_df['document'] == 'оригинал') & may_df['receiving_date'].str.contains('2021-05-')),
    ((may_df['new/current'] == 'текущая') & (may_df['status'] != 'ПРОСРОЧЕНО') &
     (may_df['document'] == 'оригинал') & may_df['receiving_date'].str.contains('2021-05-') &
     (may_df['sum'] > 10000)),
    ((may_df['new/current'] == 'текущая') & (may_df['status'] != 'ПРОСРОЧЕНО') &
     (may_df['document'] == 'оригинал') & may_df['receiving_date'].str.contains('2021-05-') &
     (may_df['sum'] < 10000))
]
choices = [
    0.07 * may_df['sum'],
    0.05 * may_df['sum'],
    0.03 * may_df['sum']
]

may_df['bonus'] = np.select(conditions, choices, default=0)
may_df = may_df[['sale', 'bonus']]
result_may = may_df.groupby('sale').sum()['bonus'].reset_index(name='bonus')


june_df = df.loc[130:257]

june_df['receiving_date'] = june_df['receiving_date'].astype(str)

conditions = [
    ((june_df['new/current'] == 'новая') & (june_df['status'] == 'ОПЛАЧЕНО') &
     (june_df['document'] == 'оригинал') & june_df['receiving_date'].str.contains('2021-06-')),
    ((june_df['new/current'] == 'текущая') & (june_df['status'] != 'ПРОСРОЧЕНО') &
     (june_df['document'] == 'оригинал') & june_df['receiving_date'].str.contains('2021-06-') &
     (june_df['sum'] > 10000)),
    ((june_df['new/current'] == 'текущая') & (june_df['status'] != 'ПРОСРОЧЕНО') &
     (june_df['document'] == 'оригинал') & june_df['receiving_date'].str.contains('2021-06-') &
     (june_df['sum'] < 10000))
]
choices = [
    0.07 * june_df['sum'],
    0.05 * june_df['sum'],
    0.03 * june_df['sum']
]

june_df['bonus'] = np.select(conditions, choices, default=0)
june_df = june_df[['sale', 'bonus']]
result_june = june_df.groupby('sale').sum()['bonus'].reset_index(name='bonus')


result_df = pd.merge(
    result_may, result_june,
    left_on='sale',
    right_on='sale',
    how='outer'
)

cols = ['bonus_x', 'bonus_y']
result_df['sum_bonus'] = result_df[cols].sum(axis=1)

print(result_df[['sale', 'sum_bonus']])
