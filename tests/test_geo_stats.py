import pytest

from geo_stats import filter_visits_by_country, query_word_stats, unique_ids


GEO_LOGS = [
    {'visit1': ['Москва', 'Россия']},
    {'visit2': ['Дели', 'Индия']},
    {'visit3': ['Владимир', 'Россия']},
    {'visit4': ['Лиссабон', 'Португалия']},
    {'visit5': ['Париж', 'Франция']},
    {'visit6': ['Волгоград', 'Россия']},
    {'visit7': ['Прага', 'Чехия']},
    {'visit8': ['Владимир', 'Россия']},
    {'visit9': ['Курск', 'Россия']},
    {'visit10': ['Флоренция', 'Италия']},
]


@pytest.mark.parametrize(
    'country, expected_visits',
    [
        (
            'Россия',
            [
                {'visit1': ['Москва', 'Россия']},
                {'visit3': ['Владимир', 'Россия']},
                {'visit6': ['Волгоград', 'Россия']},
                {'visit8': ['Владимир', 'Россия']},
                {'visit9': ['Курск', 'Россия']},
            ],
        ),
        (
            'Индия',
            [{'visit2': ['Дели', 'Индия']}],
        ),
        (
            'Италия',
            [{'visit10': ['Флоренция', 'Италия']}],
        ),
        (
            'Япония',
            [],
        ),
    ],
)
def test_filter_visits_by_country(country, expected_visits):
    assert filter_visits_by_country(GEO_LOGS, country) == expected_visits


@pytest.mark.parametrize(
    'ids, expected',
    [
        (
            {
                'user1': [213, 213, 213, 15, 213],
                'user2': [54, 54, 119, 119, 119],
                'user3': [213, 98, 98, 35],
            },
            {213, 15, 54, 119, 98, 35},
        ),
        (
            {'user1': [1, 1, 1], 'user2': [1, 2]},
            {1, 2},
        ),
        (
            {'user1': []},
            set(),
        ),
    ],
)
def test_unique_ids(ids, expected):
    assert unique_ids(ids) == expected


@pytest.mark.parametrize(
    'queries, expected',
    [
        (
            [
                'смотреть сериалы онлайн',
                'новости спорта',
                'афиша кино',
                'курс доллара',
                'сериалы этим летом',
                'курс по питону',
                'сериалы про спорт',
            ],
            {2: 42.86, 3: 57.14},
        ),
        (
            ['один', 'два слова', 'ещё два'],
            {1: 33.33, 2: 66.67},
        ),
        (
            [],
            {},
        ),
    ],
)
def test_query_word_stats(queries, expected):
    assert query_word_stats(queries) == expected
