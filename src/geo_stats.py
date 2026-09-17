"""Задание из лекции 1.4 «Циклы. Типы данных. Коллекции данных»."""


def filter_visits_by_country(geo_logs, country='Россия'):
    filtered = []
    for visit in geo_logs:
        for places in visit.values():
            if places and places[-1] == country:
                filtered.append(visit)
    return filtered


def unique_ids(ids):
    result = set()
    for numbers in ids.values():
        result.update(numbers)
    return result


def query_word_stats(queries):
    if not queries:
        return {}

    counts = {}
    for query in queries:
        words_count = len(query.split())
        counts[words_count] = counts.get(words_count, 0) + 1

    total = len(queries)
    return {
        words_count: round(count / total * 100, 2)
        for words_count, count in counts.items()
    }
