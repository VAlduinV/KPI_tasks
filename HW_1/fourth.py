import logging
import pandas as pd
import matplotlib.pyplot as plt
import mplcyberpunk

plt.style.use("cyberpunk")

# Ініціалізація системи логування з режимом запису 'w' (перезапис)
logging.basicConfig(filename='neuron_analysis.log', level=logging.INFO, encoding='utf-8', filemode='w')  # Додайте filemode='w'

# Завантаження даних з файлу з вказанням кодування
data = pd.read_csv('NeuronRecords.csv', encoding='utf-8')  # Замініть 'NeuronRecords.csv' на відповідний шлях до вашого файлу

# Перегляд першого стовпця даних (часу)
time = data['time']

# Перегляд і аналіз кожного стовпця з потенціалом нейрона
for col in data.columns[1:]:  # Проходимо по всіх стовпцях, крім першого (часу)
    neuron_potential = data[col]

    # Знаходимо мінімум та максимум для потенціалу нейрона
    min_potential = neuron_potential.min()
    max_potential = neuron_potential.max()

    # Логуємо результати
    logging.info(f"Мінімум для {col}: {min_potential}")
    logging.info(f"Максимум для {col}: {max_potential}")

    # Побудова графіка ISI (міжспайковий інтервал)
    plt.figure(figsize=(10, 5))
    plt.plot(time, neuron_potential)
    plt.xlabel('Час')
    plt.ylabel('Потенціал нейрона')
    plt.title(f'Графік потенціалу нейрона для {col}')
    mplcyberpunk.add_glow_effects()
    plt.show()
