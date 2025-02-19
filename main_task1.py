import argparse
from pathlib import Path
from shutil import copyfile
from threading import Thread
import logging
import os

# Опис аргументів командного рядка
parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--source", "-s", help="Source folder", required=True)
parser.add_argument("--output", "-o", help="Output folder", default="dist")

args = parser.parse_args()
source = Path(args.source)
output = Path(args.output)

# Перевірка наявності папки "output", створення якщо її немає
output.mkdir(exist_ok=True)

folders_to_process = [source]  # Список папок для обробки

# Логування для зручності
logging.basicConfig(level=logging.INFO, format="%(threadName)s %(message)s")


def create_folder_list(path: Path) -> None:
    """
    Функція для рекурсивного отримання всіх папок.
    """
    for el in path.iterdir():
        if el.is_dir():
            folders_to_process.append(el)
            create_folder_list(el)


def copy_file(path: Path) -> None:
    """
    Функція для копіювання файлів за їхнім розширенням.
    """
    for el in path.iterdir():
        if el.is_file():
            ext = el.suffix[1:]  # Отримання розширення файлу
            if ext:  # Якщо розширення не порожнє
                ext_folder = output / ext
                ext_folder.mkdir(exist_ok=True, parents=True)  # Створення папки для розширення, якщо не існує
                try:
                    copyfile(el, ext_folder / el.name)  # Копіювання файлу
                    logging.info(f"Файл {el.name} скопійовано в {ext_folder}")
                except OSError as err:
                    logging.error(f"Помилка копіювання файлу {el.name}: {err}")

if __name__ == "__main__":
    # Отримання всіх папок
    create_folder_list(source)

    # Створення потоків для кожної папки
    threads = []
    for folder in folders_to_process:
        th = Thread(target=copy_file, args=(folder,))
        th.start()
        threads.append(th)

    # Очікування завершення всіх потоків
    for th in threads:
        th.join()

    logging.info(f"Обробка завершена. Папка {source} скопійована в папку {output}")
