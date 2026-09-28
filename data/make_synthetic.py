"""
Генератор СИНТЕТИЧЕСКИХ данных для демонстрационных ноутбуков demo-01 и demo-05.

ВНИМАНИЕ: это заглушки. Настоящие показания гравиметра и экспериментальные
записи движения человека в репозитории отсутствуют. Если примеры останутся
в курсе, файлы нужно заменить реальными данными того же формата.

Запуск из корня репозитория:  python data/make_synthetic.py
"""
import numpy as np

rng = np.random.default_rng(2026)   # фиксированное зерно: файлы воспроизводимы


def make_gravimeter(path='data/gravimeter_synthetic.txt'):
    """Два канала «показаний гравиметра»: медленная аномалия + сильный шум.

    Формат: столбцы t [с], g1 [мГал], g2 [мГал]; строки через пробел.
    """
    dt = 1.0                              # такт съёма, с
    t = np.arange(0.0, 3600.0, dt)        # один час записи
    # полезный сигнал: гравитационная аномалия, мГал
    signal = 20 * np.sin(2 * np.pi * t / 1800) + 15 * np.exp(-((t - 2200) / 250) ** 2)
    channels = []
    for _ in range(2):
        # «помехи»: белый шум + медленный дрейф + колебания носителя
        noise = (100 * rng.standard_normal(t.size)
                 + 5 * np.cumsum(rng.standard_normal(t.size)) / np.sqrt(t.size)
                 + 60 * np.sin(2 * np.pi * t / 17 + rng.uniform(0, 2 * np.pi)))
        channels.append(signal + noise)
    data = np.column_stack([t, *channels])
    header = ('СИНТЕТИЧЕСКИЕ ДАННЫЕ (заглушка, см. data/make_synthetic.py)\n'
              'столбцы: t [c], g1 [мГал], g2 [мГал]')
    np.savetxt(path, data, fmt='%.3f', header=header, encoding='utf-8')
    return data


def make_adc(path='data/adc_synthetic.txt'):
    """Координаты точек тела при вставании со стула и приседании (профиль).

    Формат повторяет файл adc.txt из MATLAB-версии курса: строка --- момент
    времени (шаг 0.01 с), координаты точки занимают два соседних столбца
    (x, y), мм. Номера столбцов x (с единицы, как в MATLAB):
    плечо 23, корпус 20, тазобедренный сустав 17, колено 14, щиколотка 11,
    пальцы стопы 8. Столбец 1 --- время, прочие столбцы заполнены нулями.
    """
    n_rows, n_cols = 900, 26
    t = np.arange(n_rows) * 0.01
    # фаза движения s: 0 --- сидя, 1 --- стоя (встать за 3 с, постоять, сесть)
    s = np.interp(t, [0, 1, 4, 5, 8, 9], [0, 0, 1, 1, 0, 0])
    s = 0.5 - 0.5 * np.cos(np.pi * s)                 # сглаживание
    L_shank, L_thigh, L_trunk = 430.0, 430.0, 520.0   # длины звеньев, мм
    toe = np.array([0.0, 0.0])
    ankle = np.array([-150.0, 80.0])
    th_s = np.radians(10 * (1 - s))                   # наклон голени от вертикали
    phi = np.radians(90 * s)                          # подъём бедра от горизонтали
    psi = np.radians(20 * (1 - s) + 35 * np.sin(np.pi * s))   # наклон корпуса
    knee = ankle + L_shank * np.column_stack([np.sin(th_s), np.cos(th_s)])
    hip = knee + L_thigh * np.column_stack([-np.cos(phi), np.sin(phi)])
    trunk = hip + 0.5 * L_trunk * np.column_stack([np.sin(psi), np.cos(psi)])
    shoulder = hip + L_trunk * np.column_stack([np.sin(psi), np.cos(psi)])
    adc = np.zeros((n_rows, n_cols))
    adc[:, 0] = t
    points = {23: shoulder, 20: trunk, 17: hip, 14: knee,
              11: np.tile(ankle, (n_rows, 1)), 8: np.tile(toe, (n_rows, 1))}
    for col, xy in points.items():                    # col --- номер с единицы
        adc[:, col - 1] = xy[:, 0]
        adc[:, col] = xy[:, 1]
    header = ('СИНТЕТИЧЕСКИЕ ДАННЫЕ (заглушка, см. data/make_synthetic.py)\n'
              'строка --- момент времени (шаг 0.01 с); x-столбцы точек (с единицы): '
              'плечо 23, корпус 20, таз 17, колено 14, щиколотка 11, стопа 8; y --- следующий столбец; мм')
    np.savetxt(path, adc, fmt='%.2f', header=header, encoding='utf-8')
    return adc


if __name__ == '__main__':
    make_gravimeter()
    make_adc()
    print('Синтетические файлы записаны в data/')
