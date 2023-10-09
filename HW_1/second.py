import pandas as pd
from matplotlib import pyplot as plt
import polars as pl
import mplcyberpunk

plt.style.use("cyberpunk")


def fnc():
    try:
        # Читання CSV файлу
        hrv = pl.read_csv('data/Official hrivnya exchange rates.csv')
        print(hrv.head())

        # Перетворення типу даних для колонки "Date"
        T_hrv = hrv.with_columns(hrv["Date"].str.strptime(pl.Date, "%d.%m.%Y", strict=False))
        hrv_rate = hrv["Official hrivnya exchange rates, UAH"] / hrv["Unit"]

        # Відображення графіку курсу євро
        plt.plot(T_hrv["Date"].to_list(), hrv_rate.to_list(), 'r', label='euro')
        plt.legend()
        plt.title('Курс Євро')
        mplcyberpunk.add_glow_effects()
        plt.show()

    except FileNotFoundError:
        print("Файл не знайдено. Переконайтеся, що шлях до файлу правильний.")
    except Exception as e:
        print(f"Виникла помилка: {e}")


def infla_df():
    """
        Дані інфляції прямо завантажити з 136-indeksi-spozhivchikh-tsin.csv
    """
    file_path = r'/HW_1/data/136-indeksi-spozhivchikh-tsin.csv'
    # Завантажте дані в DataFrame
    df = pd.read_csv(file_path)
    print(df.head())


def func_idx():
    """
        Завантажити з excel файла: https://www.ukrstat.gov.ua/operativ/open_data/2022/136.xlsx із 4-ого листа,
        вказати параметр sheet_id = 4
    """
    # Шлях до файлу на вашому комп'ютері
    file_path = r'/HW_1/data/136.xlsx'

    # Індекс листа, який вас цікавить (4-ий лист)
    sheet_id = 3  # Зауважте, що листи нумеруються з нуля

    # Завантаження даних з XLSX-файлу
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_id)
        # Операції з DataFrame
        # Наприклад, можна вивести перші 5 рядків
        print(df.head())
    except FileNotFoundError:
        print("Файл не знайдено. Переконайтеся, що шлях до файлу правильний.")
    except Exception as e:
        print(f"Виникла помилка при завантаженні та обробці даних: {e}")


if __name__ == "__main__":
    print("Table is NBU:")
    fnc()
    print("Table is 136 sheet Consumer price indices:")
    func_idx()
    print("Дані інфляції")
    infla_df()
