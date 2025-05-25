#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import simple_draw as sd

sd.resolution = (1200, 600)

# Нарисовать пузырек - три вложенных окружностей с шагом 5 пикселей
# TODO здесь ваш код
# Нарисовать пузырек - три вложенных окружностей с шагом 5 пикселей
for x in range(50, 65, 5):
    sd.circle(center_position=sd.get_point(600, 300), radius=x, width=2)


# Написать функцию рисования пузырька, принммающую 3 (или более) параметра: точка рисования, шаг и цвет
def bubble(point, step, col):

    all_col = (sd.COLOR_RED, sd.COLOR_ORANGE, sd.COLOR_YELLOW, sd.COLOR_GREEN,
                      sd.COLOR_CYAN, sd.COLOR_BLUE, sd.COLOR_PURPLE, sd.COLOR_DARK_BLUE, sd.COLOR_DARK_PURPLE, sd.COLOR_DARK_ORANGE)
    for _ in range(3):
        sd.circle(center_position=point, radius=step, color=all_col[col], width=2)

# Нарисовать 10 пузырьков в ряд
for x in range(100, 1001, 100):
    bubble(point=sd.get_point(x, 40), step=14, col=1)

# Нарисовать три ряда по 10 пузырьков
# Здесь используется вложенный цикл
for y in range(300, 501, 100):
    for x in range(100, 1001, 100):
        bubble(point=sd.get_point(x, y), step=12, col=6)

# Нарисовать 100 пузырьков в произвольных местах экрана случайными цветами
import random as rnd

for _ in range(100):
    bubble(point=sd.random_point(), step=8, col=rnd.randint(0,9))

sd.pause()
