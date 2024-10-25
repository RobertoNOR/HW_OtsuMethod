from typing import List


def otsu_method(array_of_rgb: List[List[List[int]]]) -> List[List[int]]:
    """
    Преобразует цветное изображение (трехмерный массив RGB) в бинарное изображение (двумерный массив)
    при помощи метода Отсу.

    Параметры:
    ---------
    array_of_rgb: List[List[List[int]]]
        Трёхмерный список, где каждый элемент — это список значений интенсивности для каждого канала RGB.

    Возвращает:
    ----------
    List[List[int]]
        Двумерный список, содержащий бинарные значения пикселей для каждой строки.
    """

    # Преобразование RGB в градации серого с использованием формулы для яркости
    convert_to_gray = [
        [round(0.299 * r + 0.587 * g + 0.114 * b) for r, g, b in row]
        for row in array_of_rgb
    ]

    # Инициализация гистограммы интенсивностей
    h = [0] * 256
    # Заполнение гистограммы
    for i in convert_to_gray:
        for j in i:
            h[j] += 1

    # Вычисление вероятностей для каждой интенсивности
    p = [h_i / sum(h) for h_i in h]

    # Расчет взвешенных накопленных вероятностей для классов 0 и 1
    w_0 = [sum(p[:i]) for i in range(256)]  # Вес первого класса
    w_1 = [sum(p[i:]) for i in range(256)]  # Вес второго класса

    # Инициализация массивов для средних значений классов
    u_0 = [0] * 256
    u_1 = [0] * 256
    # Расчет средних значений для классов 0 и 1
    for t in range(256):
        u_0[t] = sum(i * p[i] for i in range(t)) / w_0[t] if w_0[t] != 0 else 0
        u_1[t] = sum(i * p[i] for i in range(t, 256)) / w_1[t] if w_1[t] != 0 else 0

    # Вычисление межклассовой дисперсии
    d = [w_0[i] * w_1[i] * pow(u_0[i] - u_1[i], 2) for i in range(256)]

    # Поиск оптимального порога (максимум межклассовой дисперсии)
    t = d.index(max(d))

    # Преобразование изображения в бинарное по найденному порогу
    array_of_binary = [
        [1 if pixel > t else 0 for pixel in i]
        for i in convert_to_gray
    ]

    return array_of_binary
