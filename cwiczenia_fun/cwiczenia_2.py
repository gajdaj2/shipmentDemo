def next(n):
    digits = list(str(n))

    pivot = len(digits) - 2
    while pivot >= 0 and digits[pivot] >= digits[pivot + 1]:
        pivot -= 1

    if pivot < 0:
        return -1

    swap_index = len(digits) - 1
    while digits[swap_index] <= digits[pivot]:
        swap_index -= 1

    digits[pivot], digits[swap_index] = digits[swap_index], digits[pivot]
    digits[pivot + 1 :] = sorted(digits[pivot + 1 :])

    return int("".join(digits))


print(next(513))
