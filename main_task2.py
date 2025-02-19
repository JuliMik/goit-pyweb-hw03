import time
from multiprocessing import Pool, cpu_count


# Функція для знаходження дільників числа
def find_factors(n):
    factors = []
    for i in range(1, n + 1):
        if n % i == 0:
            factors.append(i)
    return factors


# Функція для факторизації списку чисел
def factorize(*numbers):
    return [find_factors(n) for n in numbers]


# Функція для факторизації списку чисел з паралельним виконанням
def factorize_parallel(*numbers):
    with Pool(cpu_count()) as pool:
        return pool.map(find_factors, numbers)


if __name__ == '__main__':
    # Замір часу виконання
    start_time = time.time()

    a, b, c, d = factorize(128, 255, 99999, 10651060)

    end_time = time.time()
    print("Time for synchronous version: {:.6f} seconds".format(end_time - start_time))

    # Перевірка результатів
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
                 1521580, 2130212, 2662765, 5325530, 10651060]

    # Замір часу виконання паралельної версії
    start_time = time.time()

    a, b, c, d = factorize_parallel(128, 255, 99999, 10651060)

    end_time = time.time()
    print("Time for parallel version: {:.6f} seconds".format(end_time - start_time))

    # Перевірка результатів
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
                 1521580, 2130212, 2662765, 5325530, 10651060]
