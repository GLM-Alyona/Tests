"""Задание из лекции 1.3 «Введение в типы данных и циклы»: идеальные пары."""


def make_ideal_pairs(boys, girls):
    if len(boys) != len(girls):
        return 'Кто-то может остаться без пары!'

    return [
        f'{boy} и {girl}'
        for boy, girl in zip(sorted(boys), sorted(girls))
    ]
