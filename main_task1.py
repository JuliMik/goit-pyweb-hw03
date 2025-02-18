import argparse
import logging
from pathlib import Path
from shutil import copyfile
from concurrent.futures import ThreadPoolExecutor, as_completed


"""
--source [-s] 
--output [-o] default folder = dist
"""

# Створюємо парсер аргументів
parser = argparse.ArgumentParser(description="Sorting folder")
# Додаємо аргументи
parser.add_argument("--source", "-s", help="Source folder", required=True)
parser.add_argument("--output", "-o", help="Output folder", default="dist")
# Обробляємо аргументи
args = vars(parser.parse_args())

source = Path(args.get("source"))
output = Path(args.get("output"))

# Налаштовуємо логування
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(threadName)s %(message)s")


# Створюємо список директорій
def create_folders_list(path: Path) -> list:
    folders = []
    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            folders.extend(create_folders_list(el))
    return folders


# Копіюємо файли
def copy_file(el: Path) -> None:
    if el.is_file():
        ext = el.suffix[1:]
        ext_folder = output / ext
        try:
            ext_folder.mkdir(exist_ok=True, parents=True)
            copyfile(el, ext_folder / el.name)
            logging.info(f"Файл {el.name} скопійовано в {ext_folder}")
        except OSError as err:
            logging.error(f"Не вдалося скопіювати {el}: {err}")

if __name__ == "__main__":
    # Перевірка наявності вихідної папки
    if not source.exists() or not source.is_dir():
        logging.error(f"Вихідна папка {source} не існує або не є директорією.")
        exit(1)

    output.mkdir(exist_ok=True)

    folders = [source] + create_folders_list(source)

    logging.info(f"Знайдено {len(folders)} папок для обробки.")

    # Використовуємо ThreadPoolExecutor для кращого керування потоками
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(copy_file, el) for folder in folders for el in folder.iterdir()]
        for future in as_completed(futures):
            future.result()  # Для отримання потенційних винятків

    logging.info(f"Папка {source} повність скопфйована!")
