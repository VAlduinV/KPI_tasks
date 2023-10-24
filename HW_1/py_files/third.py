import polars as pl
# Візуалізувати дані
import matplotlib.pyplot as plt
import numpy as np
import mplcyberpunk

plt.style.use("cyberpunk")

"""
     Завдання 3 із завантаження даних
     Завантажте дані по вказаному посиланню, відкрийте як csv файл, в параметрах функції 
     вкажіть що немає заголовка в першому рядку через додатковий параметр has_header = False, виведіть кілька рядків таблиці.
     https://raw.githubusercontent.com/karlrupp/microprocessor-trend-data/master/50yrs/transistors.dat
"""

# Завантажити дані CSV без заголовка
data = pl.read_csv(
     'https://raw.githubusercontent.com/karlrupp/microprocessor-trend-data/master/50yrs/transistors.dat',
     has_header=False
)

# Перейменувати стовпці та перетворити їх до потрібних типів
df = data.select(pl.col('column_1').str.splitn(' ', 2).struct.rename_fields(['date', 'value'])).unnest("column_1")
df = df.select(
     pl.col('date').cast(pl.Float64, strict=False),
     pl.col('value')
)


plt.figure(figsize=(8, 6))
plt.plot(df['date'], np.asarray(df['value'].to_list(), float), 'o')
plt.yscale("log")
plt.xlabel('Рік')
plt.ylabel('Кількість транзисторів (логарифмічна шкала)')
plt.title('Динаміка кількості транзисторів з часом')
plt.grid(True)
mplcyberpunk.add_glow_effects()
plt.show()
