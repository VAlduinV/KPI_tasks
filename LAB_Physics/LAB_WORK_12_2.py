import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
import mplcyberpunk

plt.style.use("cyberpunk")


# Функція для апроксимації
def func(x, a):
    return a / x ** 2


# Завантажити дані з Excel-файлу
file_path = '../Іванов_Віктор.xlsx'
df = pd.read_excel(file_path)
print(df.columns)

# Відділіть дані зі стовпців "h, мм" і "F, Н" / "J, А/м3"
distance = df['h, мм'].to_numpy()
force = df['F, Н'].to_numpy()

# Початкове наближення для апроксимації
p0 = [1]

# Апроксимація для F(h)
popt, _ = curve_fit(func, distance, force, p0=p0)

# Графік для F(h)
plt.figure(figsize=(10, 5))
plt.scatter(distance, force, marker='o', color='b', label='Експериментальні дані')
plt.plot(distance, func(distance, *popt), 'r', label=f'Апроксимація: a/x^2, a={popt[0]:.2f}')
plt.title('Залежність F від h')
plt.xlabel('h, мм')
plt.ylabel('F, Н')
plt.grid(True)
legend = plt.legend(frameon=True)
frame = legend.get_frame()
frame.set_facecolor('black')
frame.set_edgecolor('red')
frame.set_linewidth(2)
for text in legend.get_texts():
    text.set_color('red')
mplcyberpunk.add_glow_effects()
plt.show()

# Графік для J(h)
j_data = df['J, А/м3'].to_numpy()
plt.figure(figsize=(10, 5))
plt.scatter(distance, j_data, marker='o', color='b', label='Експериментальні дані')
plt.plot(distance, j_data, 'g-', label='Дані J')
plt.title('Залежність J від h')
plt.xlabel('h, мм')
plt.ylabel('J, А/м^3')
plt.grid(True)
legend = plt.legend(frameon=True)
frame = legend.get_frame()
frame.set_facecolor('black')
frame.set_edgecolor('red')
frame.set_linewidth(2)
for text in legend.get_texts():
    text.set_color('red')
mplcyberpunk.add_glow_effects()
plt.show()
