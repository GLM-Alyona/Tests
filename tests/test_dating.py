import pytest

from dating import make_ideal_pairs


@pytest.mark.parametrize(
    'boys, girls, expected',
    [
        (
            ['Peter', 'Alex', 'John', 'Arthur', 'Richard'],
            ['Kate', 'Liza', 'Kira', 'Emma', 'Trisha'],
            [
                'Alex и Emma',
                'Arthur и Kate',
                'John и Kira',
                'Peter и Liza',
                'Richard и Trisha',
            ],
        ),
        (
            ['Ivan', 'Petr'],
            ['Anna', 'Olga'],
            ['Ivan и Anna', 'Petr и Olga'],
        ),
        (
            ['Борис'],
            ['Анна'],
            ['Борис и Анна'],
        ),
    ],
)
def test_make_ideal_pairs_success(boys, girls, expected):
    assert make_ideal_pairs(boys, girls) == expected


@pytest.mark.parametrize(
    'boys, girls',
    [
        (['Peter', 'Alex'], ['Kate']),
        (['Peter'], ['Kate', 'Liza']),
        ([], ['Kate']),
        (['Peter'], []),
    ],
)
def test_make_ideal_pairs_unequal_length(boys, girls):
    assert make_ideal_pairs(boys, girls) == 'Кто-то может остаться без пары!'
