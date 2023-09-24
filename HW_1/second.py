import pandas as pd


def fnc():
    """
    Курс гривні перейти на сторінку https://bank.gov.ua/ua/markets/exchangerate-chart?cn%5B%5D=EUR&startDate=01.01
    .1999&endDate= , завантажити собі на локальний комп'ютер в файл Official_hrivnya.csv,
    перенести файл в Google Colab і відкрити звідти.
    """
    # Шлях до файлу на вашому локальному комп'ютері
    file_path = r'C:\Users\prime\PycharmProjects\KPI_tasks\HW_1\Official_hrivnya.csv'

    # Завантажуємо CSV-файл у DataFrame
    try:
        df = pd.read_csv(file_path)
        # Операції з DataFrame
        # Наприклад, можна вивести перші 5 рядків
        print(df.head())
    except FileNotFoundError:
        print("Файл не знайдено. Переконайтеся, що шлях до файлу правильний.")
    except Exception as e:
        print(f"Виникла помилка при читанні файлу: {e}")


def infla_df():
    """
        Дані інфляції прямо завантажити з 136-indeksi-spozhivchikh-tsin.csv
    """
    file_path = r'C:\Users\prime\PycharmProjects\KPI_tasks\HW_1\136-indeksi-spozhivchikh-tsin.csv'
    # Завантажте дані в DataFrame
    df = pd.read_csv(file_path)
    print(df.head())


def func_idx():
    """
        Завантажити з excel файла: https://www.ukrstat.gov.ua/operativ/open_data/2022/136.xlsx із 4-ого листа,
        вказати параметр sheet_id = 4
    """
    # Шлях до файлу на вашому комп'ютері
    file_path = r'C:\Users\prime\PycharmProjects\KPI_tasks\HW_1\136.xlsx'

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
