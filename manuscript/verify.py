import argparse
from fractions import Fraction
import json
from math import isqrt
from pathlib import Path


def integer_cuberoot(value):
    lower = 0
    upper = 1 << ((value.bit_length() + 2) // 3)
    while lower < upper:
        middle = (lower + upper + 1) // 2
        if middle ** 3 <= value:
            lower = middle
        else:
            upper = middle - 1
    return lower


def threshold_index(index, degree):
    def admissible(candidate):
        if degree == 3:
            return index ** 3 < 3 * (candidate + 1) * (candidate + 2) * (candidate + 3)
        return index ** 2 < 2 * (candidate + 1) * (candidate + 2)

    lower = 1
    upper = max(1, index)
    assert admissible(upper)
    while lower < upper:
        middle = (lower + upper) // 2
        if admissible(middle):
            upper = middle
        else:
            lower = middle + 1
    assert admissible(lower)
    assert lower == 1 or not admissible(lower - 1)
    return lower


def integer_target_floor(target, scale):
    numerator = integer_cuberoot(target * scale ** 3 // 3)
    lower = Fraction(numerator, scale)
    upper = Fraction(numerator + 1, scale)
    assert 3 * lower ** 3 <= target < 3 * upper ** 3
    bound_lower = lower + 1 / (3 * upper)
    bound_upper = upper + 1 / (3 * lower)
    floor_lower = bound_lower.numerator // bound_lower.denominator
    floor_upper = bound_upper.numerator // bound_upper.denominator
    assert floor_lower == floor_upper
    return floor_lower


def generalized_checks(limit, scale):
    for target in range(1, limit + 1):
        value = integer_target_floor(target, scale)
        assert 3 * (value ** 3 - value) <= target
        assert target < 3 * ((value + 1) ** 3 - value - 1)
        index = max(1, value - 1)
        assert target < 3 * (index + 1) * (index + 2) * (index + 3)
        assert index == 1 or 3 * index * (index + 1) * (index + 2) <= target
    for index in range(1, limit + 1):
        value = integer_target_floor(18 * index, scale) - 1
        assert value * (value + 1) * (value + 2) <= 6 * index
        assert 6 * index < (value + 1) * (value + 2) * (value + 3)
        root = integer_cuberoot(6 * index + 6)
        wu_value = root if root * (root + 1) * (root + 2) <= 6 * index else root - 1
        assert wu_value == value
    return {
        'integer_target_inversion': {'first_M': 1, 'last_M': limit},
        'general_residual_threshold': {'first_M': 1, 'last_M': limit},
        'tetrahedral_formulas': {'first_N': 1, 'last_N': limit, 'T_0': 0},
    }


def check(limit):
    scale = 10 ** 45
    root_lower_numerator = integer_cuberoot(scale ** 3 // 3)
    assert 3 * root_lower_numerator ** 3 < scale ** 3
    assert scale ** 3 < 3 * (root_lower_numerator + 1) ** 3
    root_lower = Fraction(root_lower_numerator, scale)
    root_upper = Fraction(root_lower_numerator + 1, scale)
    values = []
    for index in range(1, limit + 2):
        actual = threshold_index(index, 3)
        values.append(actual)
        if index >= 3:
            bound_lower = root_lower * index + root_lower ** 2 / index - 1
            bound_upper = root_upper * index + root_upper ** 2 / index - 1
            floor_lower = bound_lower.numerator // bound_lower.denominator
            floor_upper = bound_upper.numerator // bound_upper.denominator
            assert floor_lower == floor_upper == actual, ('cubic', index)
        if index >= 2:
            radicand = Fraction(index ** 2, 2) + 1
            sqrt_lower_numerator = isqrt(radicand.numerator * scale ** 2 // radicand.denominator)
            sqrt_lower = Fraction(sqrt_lower_numerator, scale)
            sqrt_upper = Fraction(sqrt_lower_numerator + 1, scale)
            lower_bound = sqrt_lower - Fraction(1, 2)
            upper_bound = sqrt_upper - Fraction(1, 2)
            formula_value = lower_bound.numerator // lower_bound.denominator
            assert formula_value == upper_bound.numerator // upper_bound.denominator
            assert formula_value == threshold_index(index, 2), ('quadratic', index)
    assert values[:4] == [1, 1, 1, 1]
    assert all(values[index + 1] - values[index] in (0, 1) for index in range(limit))
    quadratic_values = [threshold_index(index, 2) for index in range(1, limit + 2)]
    assert all(quadratic_values[index + 1] - quadratic_values[index] in (0, 1) for index in range(limit))
    for candidate in range(1, 101):
        cubic_sum = sum((Fraction(1, height * (height + 1) * (height + 2) * (height + 3)) for height in range(1, candidate + 1)), Fraction())
        quadratic_sum = sum((Fraction(1, height * (height + 1) * (height + 2)) for height in range(1, candidate + 1)), Fraction())
        assert Fraction(1, 18) - cubic_sum == Fraction(1, 3 * (candidate + 1) * (candidate + 2) * (candidate + 3))
        assert Fraction(1, 4) - quadratic_sum == Fraction(1, 2 * (candidate + 1) * (candidate + 2))
    comparison_agreements = 0
    for jump_index in range(1, 1001):
        target = 3 * (jump_index + 1) * (jump_index + 2) * (jump_index + 3)
        position = integer_cuberoot(target - 1)
        assert threshold_index(position, 3) == jump_index
        assert threshold_index(position + 1, 3) == jump_index + 1
        if jump_index <= 655:
            assert position == integer_cuberoot(3 * (jump_index + 2) ** 3)
            comparison_agreements += 1
        if jump_index == 656:
            assert position == 948
            assert integer_cuberoot(3 * (jump_index + 2) ** 3) == 949
        quadratic_position = isqrt(2 * (jump_index + 1) * (jump_index + 2) - 1)
        assert threshold_index(quadratic_position, 2) == jump_index
        assert threshold_index(quadratic_position + 1, 2) == jump_index + 1
    for jump_index in range(1, limit + 1):
        shifted_index = jump_index + 2
        target = 3 * (shifted_index ** 3 - shifted_index)
        beatty_value = integer_cuberoot(3 * shifted_index ** 3)
        correction = int(beatty_value ** 3 >= target)
        assert integer_cuberoot(target - 1) == beatty_value - correction
    generalization = generalized_checks(limit, scale)
    return {
        'status': 'ALL_CHECKS_OK',
        'arithmetic': 'integer inequalities and rational root enclosures; no floating point',
        'cubic_formula': {'first_n': 3, 'last_n': limit, 'cases': limit - 2},
        'quadratic_formula': {'first_n': 2, 'last_n': limit, 'cases': limit - 1},
        'boundary_values': {'a_1_to_4': values[:4], 'd_1': threshold_index(1, 2)},
        'zero_one_increments': {'first_n': 1, 'last_n': limit},
        'quadratic_zero_one_increments': {'first_n': 1, 'last_n': limit},
        'jump_formula': {'first_j': 1, 'last_j': 1000},
        'quadratic_jump_formula': {'first_j': 1, 'last_j': 1000},
        'Beatty_discrepancy_criterion': {'first_j': 1, 'last_j': limit},
        **generalization,
        'A248188_comparison': {'agreements': comparison_agreements, 'exception_j': 656, 'jump': 948, 'comparison': 949},
        'telescoping': {'first_k': 1, 'last_k': 100, 'degrees': [2, 3]},
        'coverage': 'Finite checks support the written proofs; unbounded conclusions follow from the note.'
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, default=10000)
    parser.add_argument('--output', type=Path)
    arguments = parser.parse_args()
    if arguments.limit < 3:
        parser.error('--limit must be at least 3')
    result = check(arguments.limit)
    text = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if arguments.output:
        arguments.output.write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()
