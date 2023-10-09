import polars as pl
import logging


# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Функція для нормалізації колонки 'population' на діапазон [0, 1]
def normalize_population(data):
    min_population = data['population'].min()
    max_population = data['population'].max()
    normalized_data = data.with_columns((data['population'] - min_population) / (max_population - min_population))
    return normalized_data


# Функція для стандартизації колонки 'population'
def standardize_population(data):
    mean_population = data['population'].mean()
    std_population = data['population'].std()
    standardized_data = data.with_columns((data['population'] - mean_population) / std_population)
    return standardized_data


# Функція для нормалізації колонки 'population' на [0, 1]
def normalize_population_01(data):
    normalized_data = data.with_columns(data['population'] / data['population'].max())
    return normalized_data


if __name__ == '__main__':
    # Завдання по Polars DataFrame
    '''
        Завдання 1 Операції з числовими даними
        Завантажте таблицю із числовими даними, проведіть нормалізацію та стандартизацію колонки із числовими даними, 
        додайте нові колонки до таблиці, виведіть статистику по колонкам розширеної таблиці
    '''
    # Завантаження даних з файлу
    data = pl.read_csv('data/UATown.csv')

    # Виведення початкової таблиці
    logger.info("Початкова таблиця:")
    logger.info(data)

    # Нормалізація колонки 'population' на [0, 1]
    normalized_data_01 = normalize_population_01(data)
    logger.info("Результат нормалізації колонки 'population' на [0, 1]:")
    logger.info(normalized_data_01)

    normalized_data = normalize_population(data)
    logger.info("Результат нормалізації колонки 'population':")
    logger.info(normalized_data)

    # Стандартизація колонки 'population'
    standardized_data = standardize_population(data)
    logger.info("Результат стандартизації колонки 'population':")
    logger.info(standardized_data)

    # Додавання нових колонок до таблиці
    data = data.with_columns(
        data['lat'] * data['lng'],
        data['population'] + data['population_proper']
    )

    # Логування розширеної таблиці
    logger.info("Розширена таблиця:")
    logger.info(data)

    # Логування статистики по колонкам розширеної таблиці
    logger.info("Статистика по розширеній таблиці:")
    logger.info(data.describe())
