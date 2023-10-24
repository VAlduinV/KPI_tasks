import pandas as pd

# Завантажте XLSX файл
xlsx_file = '.xlsx'  # Замініть на шлях до вашого XLSX файлу

# Зчитайте XLSX файл
data = pd.read_excel(xlsx_file)

# Збережіть дані у файл CSV
csv_file = '.csv'  # Замініть на ім'я, під яким ви хочете зберегти файл CSV
data.to_csv(csv_file, index=False)