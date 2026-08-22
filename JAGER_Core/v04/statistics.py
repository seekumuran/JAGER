import math


def mean(values):
    if not values:
        return 0.0

    return sum(values) / len(values)


def variance(values):
    if len(values) < 2:
        return 0.0

    average = mean(values)

    return sum(
        (value - average) ** 2
        for value in values
    ) / (len(values) - 1)


def standard_deviation(values):
    return math.sqrt(
        variance(values)
    )


def rate(successes, total):
    if total == 0:
        return 0.0

    return successes / total
